#include "extractor/jni_extractor.h"
#include <string.h>
#include <iostream>
#include "logging.h"
#include "jvm_mocks.h"
#include "jnienv_mokcs.h"

using namespace extr_jni;

/* Global Methods implementation */

// This vector is used by DynamicExtractor to
// Store the currently extracted JavaNativeMethods
std::vector<JNINativeMethod> registered_methods_;

jclass FakeFindClass(JNIEnv *env, const char *clazz) { return NULL; }

jint FakeRegisterNatives(JNIEnv *env, jclass clazz,
                         const JNINativeMethod *methods, jint n) {
  for (int i = 0; i < n; i++) {
    JNINativeMethod method = *(methods + i);
    registered_methods_.push_back(method);
  }

  return 0;
}

jint FakeGetEnv(JavaVM *vm, void **env, jint version) {
  JNINativeInterface *envFuncs =
      (JNINativeInterface *)malloc(sizeof(JNINativeInterface));

  // mocking RegisterNatives and FindClass to extract the jni methods
  envFuncs->RegisterNatives = &FakeRegisterNatives;
  envFuncs->FindClass = &FakeFindClass;
  // setting up the fake environment
  JNIEnv *fakeEnv = (JNIEnv *)malloc(sizeof(JNIEnv));
  fakeEnv->functions = envFuncs;

  // setting the environment to our fake one
  *env = fakeEnv;

  return 0;
}

/* DynamicExtractor Class Implementation */

// DynamicExtractor implementation
DynamicExtractor::DynamicExtractor(std::vector<std::string> &library_paths,
                                   std::string signatures_path)
    : Extractor::Extractor(library_paths, signatures_path) {
  // Nothing to do, just call the super constructor
}

DynamicExtractor::DynamicExtractor(std::vector<std::string> &library_paths,
                                   std::string signatures_path,
                                   SignatureStyle style)
    : Extractor::Extractor(library_paths, signatures_path, style) {}

bool DynamicExtractor::Extract(std::string signature, JNINativeMethod& result) {
  std::vector<std::string> paths = this->GetLibraryPaths();
  
  for (std::vector<std::string>::iterator iter = this->GetLibraryPaths().begin();
       iter != this->GetLibraryPaths().end(); iter++) {
    // We try to extract the given signature looking in all
    // the available libraries. There won't be so many
    // .so files anyway, so it should be alrigth
    std::string lib_path = *iter;

    // ExtractJni will populate registered_methods_
    // With all the method registered if any is found

    try {
      this->ExtractJni(lib_path.c_str());
      for (std::vector<JNINativeMethod>::iterator reg_iter =
               registered_methods_.begin();
           reg_iter != registered_methods_.end(); reg_iter++) {
        JNINativeMethod method = *reg_iter;
        
        // method.name is the java version of the name, which means
        // we can directly compare with the provided signature
        LOG_DEBUG("jni_dynamic_extractor - %s %s", method.name, method.signature);
        LOG_FILE_DEBUG("jni_dynamic_extractor - %s %s", method.name, method.signature);

        if (!strcmp(method.name, this->GetNameFromSignature(signature).c_str())) {
          result = method;
          result.signature = (char *) malloc(signature.size() + 1);
          strncpy((char*) result.signature, signature.c_str(), signature.size() + 1);
          LOG_DEBUG("jni_dynamic_extractor - found %x", method.fnPtr);
          return true;
        }
      }
    } catch (const libutils::LibraryOpeningError &ex) {
      LOG_ERR("%s", ex.what());
      LOG_FILE_DEBUG("%s", ex.what());
    } catch (const libutils::FunctionPointerLookupException &ex) {
      LOG_ERR("%s", ex.what());
      LOG_FILE_DEBUG("%s", ex.what());
    }
  }
  LOG_DEBUG("dynamic extraction is over");
  LOG_FILE_DEBUG("dynamic extraction is over");
  return false;
}

/* Private Method implementation follow from here */

void DynamicExtractor::ExtractJni(const char *lib_path) {
  // Create a fake JavaVm using our mocks
  JavaVM *jvm = (JavaVM *) malloc(sizeof(JavaVM*));
  jmocks::GetMockedJavaVM(&jvm);
  
  // Now we need to invoke the JNI_OnLoad method.
  typedef jint (*JNI_OnLoad_ptr)(JavaVM *, void *);

  libutils::LibUtils lib_utils(lib_path);
  JNI_OnLoad_ptr JNI_OnLoad_Func =
      (JNI_OnLoad_ptr)lib_utils.GetFunctionPtr("JNI_OnLoad");

  // After this call registered_methods_ should be populated
  JNI_OnLoad_Func(jvm, NULL);
  LOG_DEBUG("jni_dynamic_extractor JNI_OnLoad fully executed");
  registered_methods_ = emock::GetRegisteredNatives();
}