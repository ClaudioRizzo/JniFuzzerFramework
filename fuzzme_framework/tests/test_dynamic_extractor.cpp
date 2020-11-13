#include "gtest/gtest.h"
#include "extractor/jni_extractor.h"
#include <string>
#include "logging.h"

namespace {
class DynamicExtractorTests : public ::testing::Test {
 private:
  const char *lib_path_ = "extractor_test_files/libnative-lib-dynamic.so";

 public:
  void SetUp() {}

  void TearDown() {
    // code here will be called just after the test completes
    // ok to through exceptions from here if need be
  }

  std::string GetLibPath() { return this->lib_path_; }
};

// The test check that the dynamic extractor correctly extracs
// all the given (and known) jni methods added with RegisterNative.
// Since the library is self implemented, we may miss cases as we only
// mock FindClass and RegisterNatives of the Env.
TEST_F(DynamicExtractorTests, SimpleMethodsCorrectlyExtractedTest) {
    std::string empty_str;
    std::vector<std::string> library_paths;
    library_paths.push_back(this->GetLibPath());
    extr_jni::DynamicExtractor dynamic_extractor(library_paths, empty_str);
    
    JNINativeMethod method_1 = {};
    
    bool result_1 = dynamic_extractor.Extract("<uk.ac.rhul.clod.samplejniapp: void printHelloWorld(java.lang.String)>", method_1);
    ASSERT_EQ(0, strcmp(method_1.name, "printHelloWorld"));
    ASSERT_TRUE(result_1);

    JNINativeMethod method_2 = {};
    bool result_2 = dynamic_extractor.Extract("<uk.ac.rhul.clod.samplejniapp: java.lang.String getMessage()>", method_2);
    ASSERT_EQ(0, strcmp(method_2.name, "getMessage"));
    ASSERT_TRUE(result_2);

    JNINativeMethod static_method = {};
    // StringFromJNI is declared as static so we do not expect it to be extracted. An empty string is expected
    bool result_3 = dynamic_extractor.Extract("<uk.ac.rhul.clod.samplejniapp: java.lang.String stringFromJNI()>", static_method);
    ASSERT_FALSE(result_3);
}

}  // namespace