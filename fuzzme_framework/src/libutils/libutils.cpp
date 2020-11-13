#include "libutils/libutils.h"
#include <dlfcn.h>
#include <stdio.h>
#include <sstream>
#include "logging.h"

using namespace libutils;

LibUtils::LibUtils(const char *lib_path) {
  this->lib_path_ = lib_path;
  this->handle_ = NULL;
  this->OpenLibrary();
}

void *LibUtils::GetHandle() { return this->handle_; }

void *LibUtils::GetFunctionPtr(const char *function_name) {
  void *function = dlsym(this->handle_, function_name);
  const char *dlsym_error = dlerror();
  LOG_DEBUG("%s - looking for %s", this->lib_path_, function_name);
  if (dlsym_error) {
    std::ostringstream errorStream;
    errorStream << "error retrieving function " << function_name << ". "
                << "Error is:" << dlsym_error;
    LOG_ERR("%s", errorStream.str().c_str());
    throw FunctionPointerLookupException(errorStream.str().c_str());
  }
  return function;
}

void LibUtils::OpenLibrary() {
  void *handle = dlopen(this->lib_path_, RTLD_LAZY);

  if (!handle) {
    const char *dlsym_error = dlerror();
    std::ostringstream errorStream;
    errorStream << "[err] error opening the library " << this->lib_path_ << ". "
                << "Error is:" << dlsym_error << "\n";
    LOG_ERR("%s", errorStream.str().c_str());
    throw LibraryOpeningError(errorStream.str().c_str());
  }

  // reset errors
  dlerror();
  this->handle_ = handle;
}

// LibraryOpeningError implementation

LibraryOpeningError::LibraryOpeningError(const char *message) {
  this->message_ = message;
}
const char *LibraryOpeningError::what() const throw() { return this->message_; }

// FunctionPointerNotFoundException implementation

FunctionPointerLookupException::FunctionPointerLookupException(
    const char *message) {
  this->message_ = message;
}
const char *FunctionPointerLookupException::what() const throw() {
  return this->message_;
}
