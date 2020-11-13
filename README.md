# Jni Fuzzer Framework

## Setup emulator for afl-fuzzing

**Set up android emulator.** The easiest way to run experiment is via an android emulator. To create a new one follow these steps:
```bash
cd $ANDROID_HOME/tools/bin;
./sdkmanager "system-images;android-23;google_apis;armeabi-v7a"
./avdmanager create avd -n 'an_epic_name' -k 'system-images;android-23;google_apis;armeabi-v7a'
```
The command will create and avd called an_epic_name emulating armeabi-v7a with android-23 (M).
Alternatively, you can use android studio to create an avd, but I won't cover this in here (just google it, it is fairly simple 🙂)

Whatever you decide to do, make sure you use android-23 API for an armeabi-v7a ISA. This is where I tested AFL and I will assume this from now on.
At this point run the emulator: 
```bash
cd $ANDROID_HOME/emulator
./emulator @an_epic_name
```
When your emulator is ready,
`adb devices; # check that your emulator is at device status`
push afl files into it:

```bash
cd emulator;
tar -xzf afl_android.tar.gz
adb push bin /data/local/tmp
adb shell -c '/data/local/tmp/bin/afl-fuzz'
```

You are now ready to go!


**Restore existing android emulator (prefered).** On github I have provided a ready to use emulator. To install it, follow these steps:
First download the emulator tar in your home directory (or wherevere you like), by following this link: https://drive.google.com/open?id=1O7Cwr6G01hDvy9rxB-OvCUDFxYm1F3hG
```bash
cd emulator;
export ANDROID_PATH=/your/sdk/location # you may have it already set, check;
mv $HOME/afl_avd.tar.gz .
mkdir afl_avd
tar -xzf afl_avd.tar.gz --directory afl_avd
chmod +x install_emulator;
./install_emulator afl_avd

cd $ANDROID_HOME/emulator;
./emulator @an_epic_name
# wait for device

adb shell -c '/data/local/tmp/bin/afl-fuzz'
```

## Install fuzzme_framework
In this section I will detail how to install fuzzme_framework into the emulator and start fuzzing JNI method with AFL. 

TO BE CONTINUED.
