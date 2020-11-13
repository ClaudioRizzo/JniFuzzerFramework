'''
analysis
~~~~~~~~


This module collects all useful functions to be used
by the worker when performing a fuzzing analysis
'''
import os
import random
import string
from config import Config
import logging as logger
import time
import worker_timeout as wt
import shutil
import seeds_generator as sg
import ast
import numpy as np
import sklearn.feature_selection as fs
from jni_extractor.method_abstraction import SootMethod


conf = Config()

WORKSPACE = '/data/local/tmp/workspace'
LIBS = os.path.join(WORKSPACE, 'libs')
INPUT = os.path.join(WORKSPACE, 'inputs')
OUTPUT = os.path.join(WORKSPACE, 'outputs')
FUZZ_ME = os.path.join(WORKSPACE, conf.fuzz_me_bin)


class NotBootedError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class AnalysisCompleted(Exception):
    def __init__(self, message, dry_run=False):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.dry_run = dry_run


class AnalysisAborted(Exception):
    ONLY_INTEGER = 'only_int'
    TYPE_NOT_SUPPORTED = 'type_not_supported'
    ISA_NOT_FOUND = 'isa_not_found'
    DRY_RUN_ERROR = 'dry_run_error'
    EMULATOR_FAILED = 'emulator_failure'

    def __init__(self, message, code):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.code = code


class AflDryRunError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class AflDryRunSeedError(AflDryRunError):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def _check_booted(emu):
    if not emu.booted:
        logger.error("emulator {} was not booted".format(emu.name))
        raise NotBootedError("emulator {} was not booted".format(emu.name))


def gen_input_from_signature(signature):
    """Generate a random seed input and returns it as a string"""
    # TODO (clod) this method has to be thougth properly as it is crucial
    # to have proper input. For now I just use a lame random implementation
    return sg.generate_seeds(signature)


def init_emulator(emu, apk_id, signature, isa):
    """initialize the provided emulator so that
    it can perform fuzzing operations on the given signature for the library
    with the given isa.

    **NOTE** The emulator should be booted, or `NotBootedError` is thrown

    Args:
        (AndroidEmulator) emu: the emulator we want to initialize
        (str) signature: signature that needs to be fuzzed
        (str) isa: isa of the library and emulator we try to extract signature from
    pass
    """
    _check_booted(emu)

    emu.adb.run_shell_command("mkdir {}".format(WORKSPACE)) \
        .push_file_to_emu(conf.afl_path + '_' + isa, WORKSPACE) \
        .push_file_to_emu(conf.fuzz_me + '_' + isa, WORKSPACE) \
        .run_shell_command("mkdir {}".format(INPUT)) \
        .run_shell_command("mkdir {}".format(OUTPUT))

    # set up signature
    emu.adb.run_shell_command(
        "echo '{}' >> {}/signatures.txt".format(signature, WORKSPACE))

    # TODO(clod): this currently only deals with integers
    # Also, I generate all the possible combinations of (positive, negative, 0)
    # this should probably change for too long signatures as we are generating
    # 3^(#param) seed files.
    seeds = gen_input_from_signature(signature)
    if seeds is None:
        raise AnalysisAborted(
            "We currently support only Strings and integer like signatures", code=AnalysisAborted.TYPE_NOT_SUPPORTED)
    for i in range(len(seeds)):
        seed = seeds[i]
        emu.adb.run_shell_command(
            "echo '{}' >> {}/in{}".format(seed, INPUT, i))

    # set up libraries (.so)#
    server_libs_path = os.path.join(conf.libraries, apk_id, isa)

    if not os.path.isdir(server_libs_path):
        logger.error(
            "{} version of the library not found. Analysis aborted".format(isa))
        raise AnalysisAborted("{} version of the library not found. Analysis aborted".format(
            isa), code=AnalysisAborted.ISA_NOT_FOUND)

    lib_names = os.listdir(server_libs_path)
    lib_names_emu_path = list(
        map(lambda x: os.path.join(LIBS, isa, x), lib_names))
    lib_names_str = "\n".join(lib_names_emu_path)

    emu.adb.push_file_to_emu(os.path.join(conf.libraries, apk_id, isa), os.path.join(LIBS, isa)) \
        .run_shell_command("echo -n '' >> {}/libraries.txt".format(WORKSPACE)) \
        .run_shell_command("echo '{}' >> {}/libraries.txt".format(lib_names_str, WORKSPACE)) \
        .run_shell_command("echo '0' > {}/parameter".format(WORKSPACE))

    logger.info("initialized emulator {} [yes]".format(emu.name))


def clean_emulator(emu):
    """Brings the emulator to a clean state.
    It is done by deleting the workspace folder

    **NOTE** The emulator should be booted, or `NotBootedError` is thrown
    """
    _check_booted(emu)
    emu.adb.run_shell_command("rm -rf {}".format(WORKSPACE))
    logger.info("cleaned emulator {}:{} [yes]".format(emu.name, emu.port))


@wt.timeout
def _afl_analysis(db, job_id, emu, timeout=60):
    job = db.jobs.find_one({'_id': job_id})
    soot_method = SootMethod(job['data']['signature'])
    n_param = len(soot_method.get_parameter_types())

    progress = 0
    switch_param = 0

    while True:
        # (n_param + 1) so that we can detect when to all inputs at the same time
        if (progress % (timeout // (n_param + 1) )) == 0:
            # we update the param for the fuzzer
            emu.adb.run_shell_command(
                "echo '{}' > {}/parameter".format(switch_param, WORKSPACE))
            switch_param += 1

        if (progress % 10) == 0:
            # every 10 second we updated the progres
            percentage = float(progress)/timeout * 100
            if db is not None and job_id is not None:
                db.jobs.find_one_and_update(
                    {'_id': job_id}, {'$set': {'progress': percentage}})
        progress += 1
        # let's wait until the anlysis is completed (aka the timeout is triggered)
        time.sleep(1)


def start_afl_analysis(emu, db, job_id, timeout, isa):
    """Starts afl fuzzing analysis on the provided emulator.
    The analysis blocks the execution for `timeout` seconds.
    After the timeout a `AnalysisCompleted` is raised, indicating the end of the analysis.

    Notice that there are cases where the analysis could fail. In these sytuations, `AnalysisAborted` is raised.

    The analysis updates a progress in the database, which can be used to nofify the user of the current status.

    **NOTE** The emulator should be booted, or `NotBootedError` is thrown

    Param:
        (AndroidEmulator) `emu`: emulator where the analysis should run
        `timeout` (int): length in seconds of the analysis
        `db` (pymongo connection): a connection to the database where `job_id` is stored in the jobs collection
        `job_id` (str): id of the job to update

    """
    _check_booted(emu)
    emu.adb.run_shell_command(
        'cd {}; export LD_LIBRARY_PATH={}/{}; {} -i {} -o {} -t 60000 -m 50MB -n {} > {}'.format(
            WORKSPACE, LIBS, isa, './'+conf.afl_bin + '_' + isa, INPUT, OUTPUT, FUZZ_ME + '_' + isa, WORKSPACE+'/afl.log'),
        blocking=False)
    logger.info("analysis started on {} [yes]".format(emu.name))
    # TODO (clod) do a smarter timeout based on the parameters of the signature
    # under examination. However, sometimes it may require longer for some
    # reasons. Therefore, let's stick to 10mins for now
    try:
        _check_afl_dry_run(emu, timeout=600)
    except AflDryRunSeedError:
        # the seed inputs were probably causing a crash.
        # it is in principle still interesting, so we save the results
        # we raise a TimedOutExc meaning the analysis is finished
        logger.info(
            "complted with dry-run error emulator {}:{}".format(emu.name, emu.port))
        logger.warning(
            "complted with dry-run error. It usually indicates that seeds crashed or hanged the program")
        raise AnalysisCompleted(
            "complted with dry-run error emulator {}:{}".format(emu.name, emu.port), dry_run=True)

    except(AflDryRunError, wt.TimedOutExc) as ex:
        # something went badly wrong, so we need to stop the anlysis completely
        logger.exception(ex)
        logger.error("analysis aborted on emulator {}:{}".format(
            emu.name, emu.port))
        raise AnalysisAborted(
            "analysis aborted on emulator {}:{}".format(emu.name, emu.port), code=AnalysisAborted.DRY_RUN_ERROR)

    try:
        _afl_analysis(db, job_id, emu, timeout=timeout)
    except wt.TimedOutExc:
        logger.info("analysis completed on emulator {}:{}".format(
            emu.name, emu.port))
        raise AnalysisCompleted(
            "analysis completed on emulator {}:{}".format(emu.name, emu.port))


def extract_afl_analysis_result(emu, destination):
    """Extract afl analysis result to `destination`.
    If destination doesn't exists, a `ValueError` is raised

    Params:
        (str) `destination`: location where to extract the results
    """
    if not os.path.isdir(destination):
        raise ValueError(
            "destination `{}` must be an existing folder!".format(destination))

    emu.adb.pull_file_from_emu(WORKSPACE, destination)
    zip_archive = os.path.join(destination, 'workspace')
    shutil.make_archive(zip_archive, 'zip',
                        os.path.join(destination, 'workspace'))


@wt.timeout
def _check_afl_dry_run(emu, timeout=60):
    '''This method checks for afl dry run to be successful.
    If it is not, an AflDryRunError is raised.

    The method cehcks the afl.log file we use to redirect afl stdout. We look
    for specific strings that tell us the status of the fuzzer.

    To be on the safe side, we also added a timout to this method. A good timeout (seconds) comes from the assumption
    that whatever happens it should not take longer that 1min (the timeout for an hang in AFL which we setr) * #inputs
    '''
    out = ""
    while "All set and ready to roll!" not in out:
        out = emu.adb.run_and_read_shell_command(
            'cat {}'.format(WORKSPACE+'/afl.log'))
        if "PROGRAM ABORT" in out:
            logger.warning(
                "seeds lead to afl dry run failure on {}:{}".format(emu.name, emu.port))
            raise AflDryRunSeedError(
                "seeds lead to afl dry run failure on {}:{}".format(emu.name, emu.port))
        elif "SYSTEM ERROR" in out:
            logger.error("afl dry run failure on {}:{}".format(
                emu.name, emu.port))
            raise AflDryRunError(
                "afl dry run failure on {}:{}".format(emu.name, emu.port))
    logger.info("dry run emulator {}:{} [yes]".format(emu.name, emu.port))
    return True


def _generate_taint_model(io_path):
    '''Extract io.txt file and generates a model
    that can be used by flowdroid to propagate the taint

    **NOTE** This method should be called only after AnalysisCompleted
    has been triggered!!!

    Param:
        AndroidEmulator emu: android emulator instance where io.txt file 
                             has been produced.
        str io_path: Path to `io.txt`. The file should be at the same location specified for
        `extract_afl_analysis_result`.  
    '''
    f = open(io_path, 'r')

    X = None  # parameters matrix
    Y = None  # return values: starting empty
    processed = set()
    for entry in f:
        afl_entry = ast.literal_eval(entry.strip())
        
        # we do not want duplicates
        afl_tuple = tuple(afl_entry)
        if afl_tuple in processed:
            continue
        else:
            processed.add(afl_tuple)
        
        #  afl_entry[0] is the index of the fuzzed param and afl_entry[1] is the ret value
        x = np.array(afl_entry[1:len(afl_entry)-1])
        y = afl_entry[-1]

        if X is None and Y is None:
            # this is the first entry and iteration
            X = np.array(x)
            Y = np.array(y)
        else:    
            X = np.vstack((X, x))
            Y = np.append(Y, y)
    f.close()


    result = fs.mutual_info_classif(X, Y)
    result = [round(sigmoid(x), 2) for x in result]
    print(result)
    #fs.mutual_info_regression(X, Y)

def sigmoid(x):
  return 1 / (1 + np.exp(-x))