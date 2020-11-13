'''
This module is a TaintSaviour worker and has to be used on the server where
fuzzing experiments have to be run.

On an high level it is how it works.
A main process is looking for jobs to be pushed into the databes.
When a job is fetched, a new process to handle it is spawn.
The outcoume could be: success or failure.
The main process will keep looking for process which succedeed and make them
as completed. Similar, if a job failed, it will be marked as available, so
that someone else can take care of it.

**ADB Restart**
At times, it could happen that adb gets stuck for some emulators and needs to
be restarted. This cannot be done if there are process still working as it
could result in conflicts. Therefore, we use a queue of request
and if there is at least one request, we stop fetching new job and wait
for all the job in progress to finish.
When they are finished, we restart adb and go back to normal.

**Note** that this is local to the node this worker is running in.
'''
from multiprocessing import Process, Manager, Lock, cpu_count
from multiprocessing.pool import Pool

from subprocess import TimeoutExpired, CalledProcessError

from pymongo import MongoClient, ReturnDocument
import time
import pprint
import os
import signal
import logging as lg
import uuid

from android.emulator import (AndroidEmulator, EmulatorException,
                              kill_emulator_hard, clear_emulator_lock)
from android.adb_wrapper import kill_server, start_server, list_devices

from config import Config
from pprint import pformat

import worker_timeout as wt
import random
import string

import analysis
import sys


class NoDaemonProcess(Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


def perform_job(job, port_lock):

    # first we get an emulator
    child_client = MongoClient(conf.db_host,
                               username='admin',
                               password=conf.db_pwd,
                               authSource='admin',
                               ssl=True,
                               ssl_ca_certs='/etc/ssl/mongodb.pem')

    db = child_client[conf.db_name]

    emulator_port = fetch_emulator_port(port_lock)
    emu = fetch_or_create_emulator(db, emulator_port, job['data'].get('isa'))
    try:
        if emu is None:
            raise analysis.AnalysisAborted('failed to fetch or create an emulator; job_id: {}'
                                           .format(job['_id']),
                                           analysis.AnalysisAborted.EMULATOR_FAILED)

        lg.info("fetched emulator {}:{} [yes]".format(emu.name, emulator_port))
        emulator_proc = None

        emulator_proc = emu.start_emulator_no_window()
        lg.info("started emulator {}:{} [yes]".format(emu.name, emulator_port))

        # 1. we bring the emulator in to a clean state
        analysis.clean_emulator(emu)

        # 2. initialize emulator for fuzzing
        analysis.init_emulator(
            emu, job['data']['apk_id'], job['data']['signature'], job['data']['isa'])

        # 3. start analysis

        try:
            analysis.start_afl_analysis(
                emu, db, job['_id'], timeout=int(job['data']['timeout']), isa=job['data']['isa'])
        except analysis.AnalysisCompleted as compl_ex:
            # 4. retrieve results

            res_path = os.path.join(
                conf.nas, 'TaintSaviour', 'results', job['data']['apk_id'], str(job['_id']))
            if not os.path.isdir(res_path):
                os.makedirs(res_path)
            analysis.extract_afl_analysis_result(emu, res_path)

            # stop emulator
            emu.adb.stop_emulator()

            lg.info("stopped {}:{} [yes]".format(emu.name, emulator_port))

            db.jobs.update_one({'_id': job['_id']},
                               {'$set': {'status': 'success',
                                         'progress': 100,
                                         'result_path': res_path,
                                         'result_id': str(job['_id']),
                                         'utc_epoch_completed': time.time(),
                                         'dry_run': compl_ex.dry_run,
                                         }
                                })

    except (TimeoutExpired, CalledProcessError, analysis.AnalysisAborted, Exception) as ex:
        # something went badly wrong. We need to initialize a recover procedure
        # 1. update state of the job.
        # 2. kill this emulator (the hard way)
        # 3. when no more process is working, initialize an adb restart

        error_code = 'general_error'
        if isinstance(ex, analysis.AnalysisAborted):
            error_code = ex.code
        db.jobs.update_one({'_id': job['_id']},
                           {'$set': {'status': 'failed', 'progress': 0, 'failure_code': error_code}})

        if emulator_proc is not None:
            # if the pid is None, the emulator failed to start in the first
            # place
            os.kill(emulator_proc.pid, signal.SIGKILL)

        adb_restart_requests.append(os.getpid())
        lg.debug("hard restard has been triggered")
        lg.exception(ex)

    finally:
        # whatever happened, this emulator is now switched off and ready to be
        # reused
        db.emulators.find_one_and_update(
            {'name': emu.name}, {'$set': {'status': 'available'}})
        child_client.close()
        emu_ports_in_use.remove(emulator_port)


def fetch_emulator_port(lock):
    '''
        This method return the next emulator port available.
        By doing so, it also update the list of port in use.
        The procedure is serialized and thread safe assuming that
        the lock provided is the same for all the processes involved.

        Param:
            (Lock) lock shared among the process which are requesting new ports
        Return:
            (int) next emulator port available
    '''
    lock.acquire()
    last_port = 5552
    if emu_ports_in_use:
        last_port = max(emu_ports_in_use)
    port = last_port+2
    emu_ports_in_use.append(port)
    lock.release()
    lg.debug("fetching emulator on port {}".format(port))
    return port


def fetch_or_create_emulator(db, emu_port, isa):
    # available means that the emulator is powered off and ready to be used
    # for an analysis

    supported_isas = {'armeabi-v7a', 'x86_64', 'armeabi', 'x86'}
    # if the isa received is wrong, we cannot safely create or fetch an emulator
    if isa not in supported_isas:
        lg.error('fetch emulator failed due to invalid isa {}'.format(isa))
        lg.debug('fetch emulator failed due to invalid isa {}'.format(isa))
        return None

    db_emulator = db.emulators.find_one_and_update(
        {'status': 'available', 'creator': conf.node_name, 'isa': isa},
        {'$set': {'status': 'busy'}})

    emu = None  # this will contain the emulator wrapper
    if db_emulator is not None:
        lg.debug("using existing emulator {}".format(db_emulator['name']))
        emu = AndroidEmulator(db_emulator['name'], emu_port)
        if db_emulator['init']:
            emu.is_init = True

    else:
        # check if I have enough disk space to create a new one
        # (making it busy)
        lg.debug("creating new emulator")
        emu_id = db.emulators.insert_one(
            {'status': 'busy',
             'creator': conf.node_name,
             'isa': isa,
             'init': False}
        ).inserted_id

        db_emulator = db.emulators.find_one_and_update(
            {'_id': emu_id}, {"$set": {'name': str(emu_id)}})

        try:
            _isa = isa
            if isa == 'armeabi':
                # avdmanager doesn't have armeabi
                # so we use a compatible one 
                _isa = 'armeabi-v7a'
            elif isa == 'x86':
                _isa = 'x86_64'
            
            emu = AndroidEmulator(str(emu_id),
                                  emu_port,
                                  sdk_id='system-images;android-23;' +
                                         'google_apis;{}'.format(_isa),
                                  create_new=True)
        except EmulatorException as emu_ex:
            lg.debug("could not create nor fetch a new emulator")
            lg.debug(str(emu_ex))
            # We failed to create the new emulator, let's remove from the DB
            db.emulators.find_one_and_delete({'_id': emu_id})
            lg.debug("cleaning db from this emulator")
            # We were not able to fetch nor to create a new emulator
            return None
    lg.debug(
        "emulator {} properly fetced/created on port {}".format(emu.name, emu_port))
    return emu


def _ack_job_done(db, process_at_work):
    '''
        This method looks for job marked as success by their process
        and updates their status to completed, meaning we acknoledge
        the ending of it.
        It will also join the process which failed the job to the main
        thread, removing their pid from process_at_work.
    '''
    # acknolege jobs done
    jobs_done = db.jobs.find({"status": "success", "node": conf.node_name})
    _update_working_process_and_job_status(
        db, jobs_done, process_at_work, "completed")


def _check_job_failures(db, process_at_work):
    '''
        This method looks for jobs which where marked as failed.
        It will restore their status to available, so some other
        worker/emulator can try to do it.
        It will also join the process which failed the job to the main
        thread, removing their pid from process_at_work.
    '''
    jobs_failed = db.jobs.find({"status": "failed", "node": conf.node_name})
    _update_working_process_and_job_status(
        db, jobs_failed, process_at_work, "completed-failed")


def _update_working_process_and_job_status(db, jobs, process_at_work, status):
    for job in jobs:
        process_id = job['process_id']
        finished_process = process_at_work[process_id]
        finished_process.join()
        del process_at_work[process_id]
        db.jobs.update_one({'_id': job['_id']},
                           {'$set': {'status': status}})


def _clean_up_for_start(db):
    '''
    We need to make sure we are in a consistent state.
    We collect all the job on this node which are in an
    intermidiate state and reset it to "available".
    We then look for running instances of emulator and
    try to stop them so that we do not clash.
    '''
    jobs_in_progress = db.jobs.find({'$or': [{'status': 'success'},
                                             {'status': 'taken'}]})

    for job in jobs_in_progress:
        if job['status'] == 'success':
            # this job was actually completed and we want
            # to get the report and set it to completed
            # TODO (clod)
            lg.debug("job {} recovered and completed".format(str(job['_id'])))
            pass
        else:
            # here are the job that where taken, but we still have
            # not a report. So we need to re-do the job
            db.jobs.update_one({'_id': job['_id']}, {
                               '$set': {'status': 'available'}})
            lg.debug("job {} set to available".format(str(job['_id'])))

    lg.info("jobs recovered [yes]")
    emulator_running = list_devices()
    for device in emulator_running:
        kill_emulator_hard(device.split('-')[1])
    lg.info("running emulator killed [yes]")

    emulators = db.emulator.find()
    for emu in emulators:
        avd_name = emu['name']
        clear_emulator_lock(avd_name)
    lg.info("emulator locks cleared [yes]")


def look_for_jobs(max_proc):
    '''
    Query the database for a job and forwards it to the
    an available emulator
    '''
    lg.info("starting worker")
    lg.info("config:\n{}".format(pformat(conf.get_vars())))

    # Getting the maximum number of emulator to run concurrently
    lg.info("{} available for this worker".format(max_proc))

    working_process = {}
    global adb_restart_requests

    client = MongoClient(conf.db_host,
                         username='admin',
                         password=conf.db_pwd,
                         authSource='admin',
                         ssl=True,
                         ssl_ca_certs='/etc/ssl/mongodb.pem')

    db = client[conf.db_name]

    _clean_up_for_start(db)
    lg.info("consistent state created [yes]")

    while True:
        # TODO (clod)
        # check resources before getting a job and that no restart is in
        # progress!

        _check_job_failures(db, working_process)
        _ack_job_done(db, working_process)

        if len(working_process) >= max_proc:
            continue

        if adb_restart_requests and not working_process:
            # we can proceed with restarting adb as there is no
            # working process at the moment and there was at least
            # one request for restarting
            lg.info("hard restart requested")
            kill_server()
            start_server()
            # TODO (clod) before emptying the list, let's log who

            # started the request
            # let's empty the list of request
            adb_restart_requests = manager.list()
            lg.info("hard restart completed [yes]")

        if adb_restart_requests:
            # we stop getting any job until we performed a restart
            # (which means adb_restart_requests is empty)
            continue

        job = db.jobs.find_one_and_update(
            {"status": "available"},
            {"$set": {"status": "taken", "node": conf.node_name}},
            return_document=ReturnDocument.AFTER)

        if job is not None:

            # Create a process and start a new job

            p = NoDaemonProcess(target=perform_job,
                                args=(job, Lock(), ))
            p.start()
            db.jobs.update_one({'_id': job['_id']}, {
                '$set': {'process_id': p.pid}})
            working_process[p.pid] = p
            if len(working_process) >= max_proc:
                lg.debug("reached max number of working emulator. #emulator: {}, #max_proc: {}"
                         .format(len(working_process), max_proc))

        time.sleep(1)


if __name__ == "__main__":
    try:
        lg.basicConfig(format='(%(processName)s %(process)s) %(levelname)s $ %(asctime)s $ %(message)s',
                       datefmt='%d/%m/%Y %I:%M:%S %p',
                       filename='worker.log',
                       level=lg.DEBUG)

        console_log = lg.StreamHandler()
        console_log.setLevel(lg.DEBUG)
        formatter = lg.Formatter(
            '(%(processName)s %(process)s) [%(levelname)s] %(message)s')
        console_log.setFormatter(formatter)

        lg.getLogger().addHandler(console_log)

        manager = Manager()
        adb_restart_requests = manager.list()
        emu_ports_in_use = manager.list()

        conf = Config()

        WORKSPACE = '/data/local/tmp/workspace'
        LIBS = os.path.join(WORKSPACE, 'libs')
        AFL = os.path.join(WORKSPACE, conf.afl_bin)
        INPUT = os.path.join(WORKSPACE, 'inputs')
        OUTPUT = os.path.join(WORKSPACE, 'outputs')
        FUZZ_ME = os.path.join(WORKSPACE, conf.fuzz_me_bin)

        if len(sys.argv) < 2:
            max_proc = cpu_count() // 3 * 2
        else:
            max_proc = sys.argv[1]
        look_for_jobs(int(max_proc))
    except KeyboardInterrupt:
        print("bye bye")
