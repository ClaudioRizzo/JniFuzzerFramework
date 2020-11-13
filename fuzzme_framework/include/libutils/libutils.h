#ifndef _LIB_UTILS_H
#define _LIB_UTILS_H

#include <exception>

namespace libutils {
// LibUtils class definition
// This class is a collection of utility methods to load
// *.so libraries and extract function pointers from it.
//
// Main usages scenario:
//    - extract function pointer to symbol name
//
// Note: more use cases could be added min the future
class LibUtils {
 public:
  // Given a path, it opens the provided library.
  // Throws LibraryOpeningError if the library failed to open
  //
  // Params:
  //    lib_path -> path to the library to be handled
  //
  // Throws:
  //    LibraryOpeningError if the library failed to open
  LibUtils(const char *lib_path);

  // This function returns a function pointer
  // to the function which symbol name is `function_name`
  //
  // Note: the function tryes to open the library specified
  //       when LibUtils class was created.
  //       for an alternative use
  //       GetFunctionPtr(const char *function_name, const char* lib_path)`
  //
  // Parameters:
  //    function_name -> name of the function (symbol)
  // Returns:
  //    poiter to the extracted functions
  //
  // Throws:
  //     FunctionPointerLookupException if the function was not found (or failed
  //     to fetch)
  void *GetFunctionPtr(const char *function_name);

  // Returns the handle created when opening the library. If no handle was
  // created, NULL is returned.
  //
  // Parameters: N/A
  //
  // Returns:
  //    pointer to the generated handle. NULL otherwise
  void *GetHandle();

 private:
  // Handler of the library when opened
  void *handle_;
  const char *lib_path_;

  // Throws LibraryOpeningError if library not found
  // or failing to open it
  void OpenLibrary();
};

class LibraryOpeningError : std::exception {
 public:
  LibraryOpeningError(const char *message);
  const char *what() const throw();

 private:
  const char *message_;
};

class FunctionPointerLookupException : std::exception {
 public:
  FunctionPointerLookupException(const char *message);
  const char *what() const throw();

 private:
  const char *message_;
};
}  // namespace libutils
#endif