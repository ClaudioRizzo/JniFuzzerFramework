#ifndef _JNIENV_MOCKS_H
#define _JNIENV_MOCKS_H

#include <jni.h>
#include <string.h>
#include <vector>
#include <functional>


namespace emock {

// === Mocks ===
// this section containes all the `JNIEnv` functions we currently mocked

jstring NewStringUTF_Mock(JNIEnv* env, const char* str);
const char* GetStringUTFChars_Mock(JNIEnv* env, jstring string,
                                   jboolean* isCopy);
const jchar* GetStringChars_Mock(JNIEnv* env, jstring string, jboolean* isCopy);
jsize GetStringLength_Mock(JNIEnv* env, jstring string);
jsize GetStringUTFLength_Mock(JNIEnv* env, jstring string);
void ReleaseStringChars_Mock(JNIEnv* env, jstring string, const jchar* chars);
void ReleaseStringUTFChars_Mock(JNIEnv* env, jstring string, const char* chars);
void GetStringUTFRegion_Mock(JNIEnv *env, jstring str, jsize start, jsize len, char *buf);
jint RegisterNatives_Mock(JNIEnv* env, jclass clazz,
                          const JNINativeMethod* methods, jint n);
jclass FindClass_Mock(JNIEnv *env, const char *name);
jthrowable ExceptionOccurred_Mock(JNIEnv *env);
void ExceptionDescribe_Mock(JNIEnv *env);
jmethodID GetStaticMethodID_Mock(JNIEnv *env, jclass clazz,
                                        const char *name, const char *sig);
jmethodID GetMethodID(JNIEnv* env, jclass clazz, const char* name,
                      const char* sig);
jobject CallStaticObjectMethodV_Mock(JNIEnv*, jclass, jmethodID, va_list);
void DeleteLocalRef_Mock(JNIEnv *env, jobject localRef);
jint GetVersion_Mock(JNIEnv *env);

void SetByteArrayRegion_Mock(JNIEnv *env, jbyteArray array, jsize start, jsize len, const jbyte *buf);
jbyteArray NewByteArray_Mock(JNIEnv *env, jsize len);
jobject NewObjectV_Mock(JNIEnv* env, jclass clazz, jmethodID methodID, va_list args);

// === END Mocks ===

void GetMockedEnvironment(JNIEnv** env);

/// After RegisterNatives is invoked, the methods will be
/// stored into a vector. This method returns that vector
std::vector<JNINativeMethod> GetRegisteredNatives();

}  // namespace emock

#endif