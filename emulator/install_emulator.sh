#!/bin/bash

if [ -z "$1" ]; then
    echo "[usage] $0 /path/to/ArmFuzzM folder";
    echo "[help] The folder we look for is the one containing";
    echo "[help] ArmFuzzM.avd and ArmFuzzM.ini";
    echo "[goodbye] good luck!";
    exit 0;
fi

arm_fuzz=$1;

arm_fuzz_ini=$1/'ArmFuzzM.ini'
sdk_dir=$ANDROID_HOME;
config=$1/'ArmFuzzM.avd/config.ini';
hardware=$1/'ArmFuzzM.avd/hardware-qemu.ini';

aflinit_snapshot=$arm_fuzz/'snapshots/afl_init'


sed -i 's#path=.*$#path='"${HOME}"'/.android/avd/ArmFuzzM.avd#g' $arm_fuzz_ini;

echo "[info] ArmFuzzM.ini set up..."

# setup config.ini
sed -i 's#skin.path.*$#skin.path=/'"${ANDROID_HOME}"'/skins/pixel_silver#g' $config

echo "[info] config.ini set up..."

# setup hardware-quemu.ini
sed -i 's#hw.sdCard.path.*$#hw.sdCard.path = '"${HOME}"'/.android/avd/ArmFuzzM.avd/sdcard.img#g' $hardware
sed -i 's#disk.cachePartition.path.*$#disk.cachePartition.path = '"${HOME}"'/.android/avd/ArmFuzzM.avd/cache.img#g' $hardware
sed -i 's#kernel.path.*$#kernel.path = '"${ANDROID_HOME}"'/system-images/android-23/google_apis/armeabi-v7a/kernel-ranchu#g' $hardware
sed -i 's#disk.ramdisk.path.*$#disk.ramdisk.path = '"${ANDROID_HOME}"'/system-images/android-23/google_apis/armeabi-v7a/ramdisk.img#g' $hardware
sed -i 's#disk.systemPartition.initPath.*$#disk.systemPartition.initPath = '"${ANDROID_HOME}"'/system-images/android-23/google_apis/armeabi-v7a/system.img#g' $hardware
sed -i 's#disk.dataPartition.path.*$#disk.dataPartition.path = '"${HOME}"'/.android/avd/ArmFuzzM.avd/userdata-qemu.img#g' $hardware

echo "[info] hardware-quemu.ini set up"

cp -r "$(pwd)/$1"/* "$HOME/.android/avd"
echo "[info] file copied in .android. Emulator ready to use: "
echo "[cmd] "$ANDROID_HOM"/emulator/./emulator @ArmFuzzM"
echo "[good bye] good luck! "
