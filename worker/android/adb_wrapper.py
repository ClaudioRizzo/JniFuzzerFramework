import subprocess
import os
import datetime
import time

from config import Config


def start_server():
    c = Config()
    return subprocess.run([c.adb, 'start-server'], stdout=subprocess.PIPE)


def kill_server():
    c = Config()
    return subprocess.run([c.adb, 'kill-server'], stdout=subprocess.PIPE)


def list_devices():
    c = Config()
    proc = subprocess.run([c.adb, 'devices'], stdout=subprocess.PIPE)
    devices = proc.stdout.decode('utf-8')
    return list(filter(lambda x: x is not '',
                       list(map(lambda x: x.split('\t')[0],
                                devices.split('\n')[1::]
                                )
                            )
                       )
                )


class ADB():

    '''
    @param: device - the name of the device this ADB has to manage
            usually it is emulator-xxxx where xxxx is a number starting
            from 5554 and incrementing of 2 for each emulator
    '''

    def __init__(self, device):
        conf = Config()
        self.device = device
        self.dev_port = int(device.split('-')[-1])
        self.adb = conf.adb
        self.results = "" # conf.results
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.log_file_out = 'logs/adb_out_'+str(os.getpid())+'.log'
        self.log_file_err = 'logs/adb_err_'+str(os.getpid())+'.log'

    def wait_for_device(self, timeout=60):
        timeout_date = datetime.datetime.now() + \
            datetime.timedelta(seconds=timeout)
        out = ''

        while 'device' not in out:
            cmd = [self.adb, '-s', self.device, 'get-state']
            try:
                proc = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True)
                out = proc.stdout.decode('utf-8')
            except subprocess.CalledProcessError:
                if datetime.datetime.now() > timeout_date:
                    raise subprocess.TimeoutExpired(" ".join(cmd), timeout)

    def install_apk(self, apk_path, timeout=None):
        proc = subprocess.run([self.adb, '-s',
                               self.device, 'install', apk_path
                               ],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              timeout=timeout,
                              check=True)
        self._log(proc)
        return proc

    def uninstall_apk(self, apk_package, timeout=None):
        proc = subprocess.run(
            [self.adb, '-s', self.device, 'uninstall', apk_package],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=True)

        self._log(proc)
        return proc

    def monkey(self, package_name, timeout=None):
        proc = subprocess.run([self.adb, '-s', self.device, 'shell',
                               'monkey', '-p', package_name, '--throttle',
                               '2000', '100'
                               ],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              timeout=timeout, check=True)
        self._log(proc)
        return proc

    def logcat(self, file_name=None):
        logcat_file = None

        if file_name is None:
            logcat_process = subprocess.Popen(
                [self.adb, '-s', self.device, 'logcat'])
        else:
            logcat_file = open(os.path.join(self.results, file_name), 'w')
            logcat_process = subprocess.Popen(
                [self.adb, '-s', self.device, 'logcat'], stdout=logcat_file)

        return LogCat(logcat_file, logcat_process)

    def stop_logcat(self, logcat):
        logcat.log_file.close()
        logcat.pid.terminate()

    def force_logcat_stop(self, logcat):
        logcat.pid.kill()
        logcat.log_file.close()

    def clear_logs(self):
        return subprocess.run([self.adb, '-s', self.device, 'logcat', '-c'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              check=True)

    def push_file_to_emu(self, origin, destination):
        subprocess.run([self.adb, '-s', self.device,
                        'push', origin, destination],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        # to enable chaining of commands
        return self

    def pull_file_from_emu(self, origin, destination):
        subprocess.run([self.adb, '-s', self.device,
                        'pull', origin, destination],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return self

    def _writable_sdcard(self):
        subprocess.run([self.adb, '-s', self.device, 'shell',
                        'su -c "mount -o rw,remount rootfs /"'])
        subprocess.run([self.adb, '-s', self.device,
                        'shell', '"chmod 777 /mnt/sdcard"'])

    def run_shell_command(self, command, blocking=True):
        '''
        '''
        if blocking:
            subprocess.run([self.adb, '-s', self.device, 'shell', command])
        else:
            subprocess.Popen([self.adb, '-s', self.device, 'shell', command])
        return self
    
    def run_and_read_shell_command(self, command):
        '''Execute a command on the emulator and returns its output.

        **NOTE** this will block the parent process, so it is not to be used on
        last long operation unless required
        '''
        
        proc = subprocess.run([self.adb, '-s', self.device, 'shell', command],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              check=True)
        return proc.stdout.decode('utf-8')

    def setup_ca(self, cacert_path, cacert_name):
        subprocess.run([self.adb, '-s', self.device, 'shell',
                        'su', '-c', '"mount -o remount,rw /system"'])
        self.push_file_to_emu(cacert_path, '/system/etc/security/cacerts/')
        subprocess.run(
            [self.adb, '-s', self.device, 'shell', 'su', '-c',
                '"chmod 644 /system/etc/security/cacerts/'+cacert_name+'"'])
        subprocess.run([self.adb, '-s', self.device, 'shell', 'reboot'], )

    def stop_emulator(self):
        return subprocess.run([self.adb, '-s', self.device, 'emu', 'kill'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              check=True)

    def reboot_emulator(self, timeout=None):
        return subprocess.run([self.adb, '-s', self.device, 'reboot'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              timeout=timeout,
                              check=True)

    def _log(self, p):
        stdout = p.stdout.decode('utf-8')
        stderr = p.stderr.decode('utf-8')

        with open(self.log_file_out, 'a') as o:
            o.write(stdout)

        with open(self.log_file_err, 'a') as e:
            e.write(stderr)

    def wait_for_boot(self, timeout=45):
        timeout_date = datetime.datetime.now() + datetime.timedelta(
            seconds=timeout)
        boot_completed = ''
        check_boot_cmd = [self.adb, '-s', self.device,
                          'shell', 'getprop', 'init.svc.bootanim']

        while 'running' not in boot_completed:

            try:
                proc = subprocess.run(check_boot_cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      check=True)
                boot_completed = proc.stdout.decode('utf-8')

            except subprocess.CalledProcessError as e:
                if ('device offline' in e.output.decode('utf-8') or
                        'device not found' in e.output.decode('utf-8')):
                    if datetime.datetime.now() > timeout_date:
                        raise subprocess.TimeoutExpired(
                            " ".join(check_boot_cmd), timeout)  
                else:
                    raise e
            
            if datetime.datetime.now() > timeout_date:
                        raise subprocess.TimeoutExpired(
                            " ".join(check_boot_cmd), timeout)
            time.sleep(1)


class LogCat():
    def __init__(self, log_file, pid):
        self.log_file = log_file
        self.pid = pid
