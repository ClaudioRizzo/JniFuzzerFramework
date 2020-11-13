#include "jnienv_mokcs.h"
#include <logging.h>
#include "mocks/type_mocks/jni_type_mocks.h"

/// Struct modelling a jmethodID from jni.h
struct _jmethodID {
    const char *methodName;
    const char *signature;
    jclass clazz;
};

// === Mocks ===

jstring emock::NewStringUTF_Mock(JNIEnv *env, const char *str) {

    LOG_DEBUG("NewStringUTF_Mock called");
    LOG_FILE_DEBUG("NewStringUTF_Mock called");

    char *my_str = (char *)malloc(4096);
    strncpy(my_str, str, 4096);
    return new tmocks::JString(my_str);
}

const char *emock::GetStringUTFChars_Mock(JNIEnv *env, jstring string,
                                          jboolean *isCopy) {
    LOG_DEBUG("calling GetStringUTFChars_Mock");
    LOG_FILE_DEBUG("calling GetStringUTFChars_Mock");
    char *str = ((tmocks::JString *)string)->getString();
    return str;
}

void emock::GetStringUTFRegion_Mock(JNIEnv *env, jstring str, jsize start, jsize len, char *buf) {
    LOG_DEBUG("GetStringUTFRegion_Mock called");
    LOG_FILE_DEBUG("GetStringUTFRegion_Mock called");
    // we will implement it if we actually need it
}

const jchar* emock::GetStringChars_Mock(JNIEnv* env, jstring string, jboolean* isCopy){
    LOG_DEBUG("calling GetStringChars_Mock");
    LOG_FILE_DEBUG("calling GetStringChars_Mock");
    return (jchar *) env->GetStringUTFChars(string, 0);
}

jsize emock::GetStringLength_Mock(JNIEnv* env, jstring string) {
    LOG_DEBUG("calling GetStringLength_Mock %d", ((tmocks::JString *)string)->GetSize());
    LOG_FILE_DEBUG("calling GetStringLength_Mock %d", ((tmocks::JString *)string)->GetSize());
    return ((tmocks::JString *)string)->GetSize();
}

jsize emock::GetStringUTFLength_Mock(JNIEnv* env, jstring string) {
    LOG_DEBUG("calling GetStringUTFLength_Mock %d", ((tmocks::JString *)string)->GetSize());
    LOG_FILE_DEBUG("calling GetStringUTFLength_Mock %d", ((tmocks::JString *)string)->GetSize());
    return ((tmocks::JString *)string)->GetSize();
}

void emock::ReleaseStringChars_Mock(JNIEnv* env, jstring string, const jchar* chars){
    LOG_DEBUG("calling ReleaseStringChars_Mock: %s", chars);
    LOG_FILE_DEBUG("calling ReleaseStringChars_Mock: %s", chars);
    // let's not do anything for now
}

void emock::ReleaseStringUTFChars_Mock(JNIEnv* env, jstring string, const char* chars){
    LOG_DEBUG("calling ReleaseStringUTFChars_Mock: %s", chars);
    LOG_FILE_DEBUG("calling ReleaseStringUTFChars_Mock: %s", chars);
    // let's not do anything for now
}

/// vector containing all the registered methods after
/// RefisterNatives_Mock has been invoked
std::vector<JNINativeMethod> registered_jni_methods;
jint emock::RegisterNatives_Mock(JNIEnv *env, jclass clazz,
                          const JNINativeMethod *methods, jint n) {
    LOG_DEBUG("RegisterNatives_Mock");
    LOG_FILE_DEBUG("RegisterNatives_Mock");
    for (int i = 0; i < n; i++) {
        JNINativeMethod method = *(methods + i);
        registered_jni_methods.push_back(method);
        //LOG_DEBUG("method: %s", method.signature);
    }

    return 0;
}

jclass emock::FindClass_Mock(JNIEnv *env, const char *name) {
    LOG_DEBUG("FindClass_Mock called");
    LOG_FILE_DEBUG("FindClass_Mock called");
    _jclass *clazz = (_jclass *) malloc(sizeof(_jclass));

    return clazz;
}

jmethodID emock::GetStaticMethodID_Mock(JNIEnv *env, jclass clazz,
                                        const char *name, const char *sig) {
    LOG_DEBUG("GetStaticMethodID_Mock called: `%s %s`", name, sig);
    LOG_FILE_DEBUG("GetStaticMethodID_Mock called: `%s %s`", name, sig);
    jmethodID method_id = (jmethodID) malloc(sizeof(jmethodID));
    method_id->clazz = clazz;
    method_id->methodName = name;
    method_id->signature = sig;

    return method_id;
}

jmethodID emock::GetMethodID(JNIEnv *env, jclass clazz, const char *name,
                      const char *sig) {
    LOG_DEBUG("GetMethodID_Mock called: `%s %s`", name, sig);
    jmethodID method_id = (jmethodID)malloc(sizeof(jmethodID));
    method_id->clazz = clazz;
    method_id->methodName = name;
    method_id->signature = sig;

    return method_id;
}

jobject emock::CallStaticObjectMethodV_Mock(JNIEnv*, jclass, jmethodID, va_list) {
    LOG_DEBUG("CallStaticObjectMethodV_Mock called");
    LOG_FILE_DEBUG("CallStaticObjectMethodV_Mock called");
    //TODO: (clod) We need implement a logic so that we return the
    // proper jobect depending on the signature of the method call
    return new tmocks::JString("Hello World");;
}

void emock::DeleteLocalRef_Mock(JNIEnv *env, jobject localRef){
    LOG_DEBUG("DeleteLocalRef_Mock called");
    LOG_FILE_DEBUG("DeleteLocalRef_Mock called");
}

jthrowable emock::ExceptionOccurred_Mock(JNIEnv *env){
    // In this model, exceptions are never thrown
    LOG_DEBUG("ExceptionOccurred_Mock called");
    LOG_FILE_DEBUG("ExceptionOccurred_Mock called");
    return NULL;
}

void emock::ExceptionDescribe_Mock(JNIEnv *env){
    LOG_FILE_DEBUG("ExceptionDescribe_Mock called");
    LOG_DEBUG("ExceptionDescribe_Mock called");
}

jint emock::GetVersion_Mock(JNIEnv *env) {
    LOG_DEBUG("GetVersion_Mock called");
    return 0x00010007;
}

void emock::SetByteArrayRegion_Mock(JNIEnv *env, jbyteArray array, jsize start, jsize len, const jbyte *buf){
    LOG_DEBUG("SetByteArrayRegion_Mock called: %s", buf);
}

jbyteArray emock::NewByteArray_Mock(JNIEnv *env, jsize len){
    LOG_DEBUG("NewByteArray_Mock called");
    return new _jbyteArray;
}

jobject emock::NewObjectV_Mock(JNIEnv* env, jclass clazz, jmethodID methodID, va_list args) {
    LOG_DEBUG("NewObjectV_Mock called");
    return new _jobject;
}


// === End Mocks ===

std::vector<JNINativeMethod> emock::GetRegisteredNatives(){
    return registered_jni_methods;
}

void emock::GetMockedEnvironment(JNIEnv **env) {
    JNIEnv *my_env = (JNIEnv *)malloc(sizeof(JNIEnv));
    JNINativeInterface *env_funcs =
        (JNINativeInterface *)malloc(sizeof(JNINativeInterface));

    env_funcs->NewStringUTF = &emock::NewStringUTF_Mock;
    env_funcs->GetStringUTFChars = &emock::GetStringUTFChars_Mock;
    env_funcs->GetStringUTFRegion = &emock::GetStringUTFRegion_Mock;
    env_funcs->GetStringChars = &emock::GetStringChars_Mock;
    env_funcs->GetStringLength = &emock::GetStringLength_Mock;
    env_funcs->GetStringUTFLength = &emock::GetStringUTFLength_Mock;
    env_funcs->ReleaseStringChars = &emock::ReleaseStringChars_Mock;
    env_funcs->ReleaseStringUTFChars = &emock::ReleaseStringUTFChars_Mock;
    env_funcs->RegisterNatives = &emock::RegisterNatives_Mock;
    env_funcs->FindClass = &emock::FindClass_Mock;
    env_funcs->ExceptionOccurred = &emock::ExceptionOccurred_Mock;
    env_funcs->ExceptionDescribe = &emock::ExceptionDescribe_Mock;
    env_funcs->GetStaticMethodID = &emock::GetStaticMethodID_Mock;
    env_funcs->GetMethodID = &emock::GetMethodID;
    env_funcs->CallStaticObjectMethodV = &emock::CallStaticObjectMethodV_Mock;
    env_funcs->DeleteLocalRef = &emock::DeleteLocalRef_Mock;
    env_funcs->GetVersion = &emock::GetVersion_Mock;
    env_funcs->SetByteArrayRegion = &emock::SetByteArrayRegion_Mock;
    env_funcs->NewByteArray = &emock::NewByteArray_Mock;
    env_funcs->NewObjectV = &emock::NewObjectV_Mock;
    my_env->functions = env_funcs;

    *env = my_env;
}
