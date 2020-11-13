#ifndef _JVM_MOCKS_H
#define _JVM_MOCKS_H

#include <jni.h>

namespace jmocks {

// === Mocks ===
// this section containes all the `JavaVM` functions we currently mocked

jint GetEnv_Mock(JavaVM *jvm, void **env, jint version);
jint AttachCurrentThread_Mock(JavaVM *vm, JNIEnv **p_env, void *thr_args);

// === END Mocks ===

void GetMockedJavaVM(JavaVM **jvm);

}  // namespace jmocks

#endif