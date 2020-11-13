#ifndef _JNI_TYPE_MOCKS_H
#define _JNI_TYPE_MOCKS_H

#include <jni.h>
#include <string>

namespace tmocks {

class JString : public _jstring
{
  private:
    char *buff_;
    int size_;

  public:
    JString(char *str);
    JString();
    char *getString();
    int GetSize();
};

/**
 * Given a `real_input` from the fuzzer, this method converts it
 * to mock input depending on the `type` the input should be.
 * 
 * Params:
 *    string type:      the type of the input we want to convert
 *    void* real_input: real bytes provided by the fuzzer
 * 
 * Returns:
 *    void* the converted input.
 */
void* ConvertFuzzerInput(std::string type, void* real_input);

double ConvertDoubleFuzzerInput(std::string type, char* real_input);

}  // namespace tmocks

#endif