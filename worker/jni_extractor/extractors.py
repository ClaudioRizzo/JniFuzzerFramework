"""Extract JNI methods from android APK"""

import os
import shutil
import subprocess

from jni_extractor.exceptions.extractor_exceptions import (FileNotFound,
                                                           FILE_NOT_FOUND,
                                                           ToolNotFoundError,
                                                           TOOL_NOT_FOUND,
                                                           InvalidFileError,
                                                           INVALID_FILE)
from jni_extractor.method_abstraction import SootMethod, AndroMethod
from androguard.core.bytecodes.dvm import DalvikVMFormat


class MethodExtractor:

    def __init__(self):
        self.__dexFolder = None

    def __convert_to_json(self, signature):
        raise NotImplementedError("STUB METHOD")

    def getSignaturesFromFile(self, filePath):
        if filePath is None:
            raise FileNotFound('{} file path provided.'.format(filePath))

        with open(filePath, 'r') as sig_file:
            return [
                SootMethod(signature.strip())
                for signature in sig_file.readlines()
            ]

    def __check_exists(self, tool):
        cmd = [tool]

        # Call subprocess.CalledProcessError if coomand -v unzip fails
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, check=True)
        out = proc.stdout.decode('utf-8')
        if out == '-bash: {}: command not found'.format(tool):
            raise ToolNotFoundError(TOOL_NOT_FOUND.format(tool))

    # extractTo has to be be a full path to a directory!
    # Returns the path of the extract classes.dex file
    def extract_dex_file(self, apk_path, extract_to):

        # check if required programs are installed (aka unzip)
        self.__check_exists('unzip')

        if not os.path.isfile(apk_path):
            raise FileNotFound(FILE_NOT_FOUND.format(apk_path))
        elif not apk_path.endswith('.apk'):
            raise InvalidFileError(INVALID_FILE.format('apk'))

        if not os.path.isdir(extract_to):
            os.makedirs(extract_to)

        # unzip apk and get dexfile
        apk_name = os.path.basename(apk_path).split('.')[0]
        self.__dexFolder = os.path.join(extract_to, apk_name)

        save_path = os.path.abspath(self.__dexFolder)
        cmd = ['unzip', '-o', apk_path, '-d', save_path]

        # Call subprocess.CalledProcessError if unzip fails
        subprocess.run(cmd, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)

        return os.path.join(self.__dexFolder, 'classes.dex')

    def clear_dex_extraction(self):
        if self.__dexFolder is not None:
            shutil.rmtree(self.__dexFolder)
            self.__dexFolder = None

    def __native_from_androguard(self, dex_file_path):

        with open(dex_file_path, 'rb') as dex_file:
            dalvik = DalvikVMFormat(dex_file.read())

        return list(
            filter(
                lambda method: method.get_access_flags_string(
                ) == "public native", dalvik.get_methods()
            )
        )

    def get_natives_from_androguard(self, dex_file_path='', apk_path=''):
        if not os.path.isfile(dex_file_path) and not os.path.isfile(apk_path):
            raise FileNotFound(
                FILE_NOT_FOUND.format(
                    'dexFile or apkFile @:\ndexPath -> {}\napkPath -> {}'
                    .format(dex_file_path, apk_path))
            )

        elif not os.path.isfile(dex_file_path):
            dex_file_path = self.extract_dex_file(apk_path, 'tmp')

        andro_raw_methods = self.__native_from_androguard(dex_file_path)

        andro_methods = list(
            map(lambda x: AndroMethod(x.get_triple()), andro_raw_methods))
        self.clear_dex_extraction()
        return andro_methods
