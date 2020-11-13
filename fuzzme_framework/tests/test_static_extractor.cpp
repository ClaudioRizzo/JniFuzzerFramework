#include <string>
#include "gtest/gtest.h"
#include "jni_extractor.h"
#include "logging.h"

namespace {
class StaticExtractorTests : public ::testing::Test {
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
};  // namespace

TEST_F(StaticExtractorTests, ExtracSimpleMethodsTest) {
    std::vector<std::string> library_paths;
    library_paths.push_back(this->GetLibPath());
    extr_jni::StaticExtractor static_extractor(library_paths, "");
    JNINativeMethod method = {};
    bool result = static_extractor.Extract(
        "<uk.ac.rhul.clod.samplejniapp.MainActivity: java.lang.string "
        "stringFromJNI()>",
        method);
    ASSERT_TRUE(result);
    EXPECT_STREQ(method.name, "stringFromJNI");
    // EXPECT_STREQ(method.signature, "stringFromJNI"); // This will be done
    // when a proper signature support is provided

    JNINativeMethod dynamic_method = {};
    static_extractor.Extract(
        "<uk.ac.rhul.clod.samplejniapp.MainActivity: void "
        "printHelloWorld(java.lang.string)>",
        dynamic_method);
    ASSERT_FALSE(result);
}