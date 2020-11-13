#include <fstream>
#include <stdexcept>
#include "gtest/gtest.h"
#include "libutils.h"

namespace {
class LibUtilsTests : public ::testing::Test {
 private:
  const char *lib_path = "libutils_test_files/libnative-all-static-lib.so";

 public:
  LibUtilsTests() {}
  ~LibUtilsTests() {}

  const char *GetLibPath() { return this->lib_path; }

  void SetUp() {
    // code here will execute just before the tests begin
    std::ifstream f(this->lib_path);
    if (!f.good()) {
      std::ostringstream stringStream;
      stringStream << "[err] could not open required file " << this->lib_path
                   << "!";
      throw std::runtime_error(stringStream.str());
    }
  }

  void TearDown() {
    // code here will be called just after the test completes
    // ok to through exceptions from here if need be
  }
};

// Given a not existing library, we expect an error
TEST_F(LibUtilsTests, InvalidLibraryTest) {
  // Library doesn't exists, we expect a LibraryOpeningError
  EXPECT_THROW(libutils::LibUtils lib_utils("I_dont_exists.so"),
               libutils::LibraryOpeningError);
}
// Given a valid library, check if correct error is throw when
// function pointer is not found in the library
TEST_F(LibUtilsTests, InvalidFunctionTest) {
  libutils::LibUtils lib_utils(this->GetLibPath());

  // The library handle MUST not be NULL at this point
  ASSERT_TRUE(lib_utils.GetHandle());

  // foo is not in the .so, so we expect FunctionPointerLookupException
  EXPECT_THROW(lib_utils.GetFunctionPtr("foo"),
               libutils::FunctionPointerLookupException);
}

// Given a valid library and function, the function pointer is correctly
// extracted. We also test that its exectuion succedes. To this end, I packed
// the library with a sumMeMock functions which takes to int and returns their
// sum. We then execute the function expecting it to do what we know it does.
TEST_F(LibUtilsTests, ValidFunctionTest) {
  typedef int (*SumMock_ptr)(int, int);
  SumMock_ptr SumMock;

  libutils::LibUtils lib_utils(this->GetLibPath());

  // The library handle MUST not be NULL at this point
  ASSERT_TRUE(lib_utils.GetHandle());
  SumMock = (SumMock_ptr)lib_utils.GetFunctionPtr("_Z9SumMeMockii");
  ASSERT_TRUE(SumMock);

  // Just a few simple test to be sure the function pointer is correctly loaded
  EXPECT_EQ(5, SumMock(3, 2));
  EXPECT_EQ(42, SumMock(40, 2));
  EXPECT_EQ(10, SumMock(3, 7));
}
}  // namespace