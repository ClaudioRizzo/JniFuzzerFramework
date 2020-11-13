import json
import os
from pathlib import Path


class Config():
    class __Config:
        def __init__(self):
            with open('config.json', 'r') as j_file:
                j_data = json.load(j_file)
                self.sdk = j_data['sdk']
                self.adb = os.path.join(self.sdk, 'platform-tools', 'adb')
                self.aapt = j_data['aapt']
                self.emulator = os.path.join(self.sdk, 'emulator', 'emulator')
                self.avdmanager = os.path.join(self.sdk, 'tools', 'bin', 'avdmanager')
    
                # afl path on the server to push to the emulator
                self.afl_bin = 'afl-fuzz'
                self.afl_path = os.path.join(j_data['afl_path'], self.afl_bin) 
                
                self.fuzz_me_folder = j_data['fuzz_me']
                self.fuzz_me_bin = 'fuzz_me'
                self.fuzz_me = os.path.join(self.fuzz_me_folder, self.fuzz_me_bin)
                self.nas = os.path.join(str(Path.home()), 'nas')
                self.libraries = os.path.join(self.nas, j_data['libraries'])
                self.db_name = j_data["db_name"]
                self.db_pwd = j_data['db_passwd']
                self.db_host = j_data['db_host']
                self.node_name = j_data['node_name']
                self.android_sdk_home = j_data['ANDROID_SDK_HOME']
    __instance = None

    def __init__(self):
        if Config.__instance is None:
            # Create and remember instance
            Config.__instance = Config.__Config()

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

    def get_vars(self):
        return vars(self.__instance)