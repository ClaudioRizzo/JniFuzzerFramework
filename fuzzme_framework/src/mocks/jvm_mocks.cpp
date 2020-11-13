#include "mocks/jvm_mocks.h"
#include <stdlib.h>
#include "jnienv_mokcs.h"
#include "logging.h"

jint jmocks::GetEnv_Mock(JavaVM *jvm, void **env, jint version) {
    LOG_DEBUG("calling GetEnv_Mock");
    emock::GetMockedEnvironment((JNIEnv **)env);
    return 0;
}

jint jmocks::AttachCurrentThread_Mock(JavaVM *vm, JNIEnv **p_env, void *thr_args) {
    LOG_DEBUG("jvm - AttachCurrentThread_Mock called");
    return 0;
}

void jmocks::GetMockedJavaVM(JavaVM **jvm) {
    // Create a fake JavaVm and set up a fake GetEnv function
    JavaVM *localJvm = (JavaVM *)malloc(sizeof(JavaVM));
    JNIInvokeInterface *jvmFuncs =
        (JNIInvokeInterface *)malloc(sizeof(JNIInvokeInterface *));

    // jvmFuncs contains all the jvm functions defined in jni
    // We manually set them and point functions to them
    jvmFuncs->GetEnv = &jmocks::GetEnv_Mock;
    jvmFuncs->AttachCurrentThread = &jmocks::AttachCurrentThread_Mock;
    localJvm->functions = jvmFuncs;
    *jvm = localJvm;
}
