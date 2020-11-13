import subprocess
import os
from config import Config
from pathlib import Path
from android.adb_wrapper import ADB


def kill_emulator_hard(port, avd_name=None):
    '''
    This method trys to kill an emulator the hard way.
    it only needs the port as it will pgrep and find its pid
    with it. The mthods also cleans some possible crashing services.

    If `avd_name` is not None, this  method also tryes to remove
    emulators lock which would prevent new instances to start

    Param:
        (str) `port` where the emulator is running
        (str) `avd_name` name of the avd to kill
    '''

    c = Config()
    cmd = ['pgrep', '-f', 'port %s' % port]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = p.stdout.decode('utf-8').strip()
    subprocess.run(['kill', '-9', stdout])
    subprocess.run(['killall', 'emulator64-crash-service'])

    if avd_name is not None:
        clear_emulator_lock(avd_name)


def clear_emulator_lock(avd_name):
    c = Config()
    lock_file = c.android_sdk_home + '/.android/avd/' + avd_name + \
        '.avd/hardware-qemu.ini.lock'

    if os.path.isfile(lock_file):
            os.remove(lock_file)


class AndroidEmulator():
    def __init__(self, name, port, proxy='127.0.0.1:8080', sdk_id='', create_new=False):
        conf = Config()
        self.avdmanager = conf.avdmanager
        self.emulator = conf.emulator
        self.name = name
        self.proxy = proxy
        self.proxy_port = int(self.proxy.split(':')[-1])
        self.port = port
        self.adb = ADB("emulator-{}".format(port))
        self.booted = False

        # By default we assume the emulator is a "vannilla" one,
        # so we should initialize it
        self.is_init = False

        if name not in self._get_present_avds() and create_new:
            try:
                self._create_avd(name, sdk_id)
            except subprocess.TimeoutExpired as to:
                raise EmulatorException("timeout expired, faild to create avd: {}".format(str(to)))
            except Exception as ex:
                raise EmulatorException("general exeption, faild to create avd: {}".format(str(ex)))
        else:
            # if the avd was already there, we assume it was
            # already initialized at some point.
            self.is_init = True

    def _get_sdk_id(self):
        proc = subprocess.run(
            [self.avdmanager, 'create', 'avd', '-n', 'foo', '-k', '""'], 
            stderr=subprocess.PIPE)
        stderr = proc.stderr.decode('utf-8')

        # we look for the first instance using an x86 and default API
        for sdk_id in stderr.split('\n'):
            if (sdk_id.split(';')[-1] == 'x86' and
                    (sdk_id.split(';')[-2] == "default")):
                return sdk_id

        # Otherwise we return the first we find
        return stderr.split('\n')[1]

    def _get_present_avds(self):
        proc = subprocess.run(
            [self.emulator, '-list-avds'], stdout=subprocess.PIPE)
        stderr = proc.stdout.decode('utf-8')
        return stderr.split('\n')

    def _create_avd(self, name, sdk_id, ncore=2, ram_size=1024):
        if(sdk_id == ''):
            sdk_id = self._get_sdk_id()

        proc = subprocess.Popen([self.avdmanager, 'create', 'avd', '-n',
                                 name, '-k', sdk_id],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        proc.communicate(b'no')
        proc.wait(timeout=20)

        with open("{}/.android/avd/{}.avd/config.ini".format(
                Config().android_sdk_home,
                self.name),
                'a') as avd_ini:

            avd_ini.write("hw.ramSize={}\nhw.cpu.ncore={}"
                          .format(ram_size, ncore))

    def start_emulator_no_window(self):
        '''
        This method starts this emulator listening on the port this emulator
        was init with. The emulator will be started without a window instance.

        When the command to start the emulator is ran, we first wait 60sec
        for the emulator to be device, then we wait for it
        too boot for another 45 seconds. If we can't in this time, 
        a TimeoutExpired is raised.

        Returns:
            process attached to the started emulator
        '''
        emu_proc = subprocess.Popen([self.emulator, '-avd', self.name,
                                     '-port', str(self.port),
                                     '-no-snapshot-save', '-no-window', '-noaudio',
                                     '-writable-system'
                                     ],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        self.adb.wait_for_device(timeout=60)
        self.adb.wait_for_boot()
        self.booted = True
        return emu_proc

    def start_emulator_with_proxy(self, port=5554, 	no_window=True):
        proc = None
        if no_window:
            proc = subprocess.Popen([self.emulator, '-avd', self.name, '-port',
                                     str(self.port), '-no-snapshot-save',
                                     '-no-window', '-writable-system',
                                     '-http-proxy', self.proxy],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen([self.emulator, '-avd', self.name, '-port',
                                     str(port), '-no-snapshot-save',
                                     '-writable-system', '-http-proxy',
                                     self.proxy],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        self.adb.wait_for_device(timeout=60)
        self.adb.wait_for_boot()
        return proc
    
    def stop_emulator(self):
        self.adb.stop_emulator()
        self.booted = False


class EmulatorException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
