#ifndef _EXECUTOR_H
#define _EXECUTOR_H

#include "jni.h"
#include "string"
#include "vector"

namespace executor {

class Executor {
   public:
    /**
     *   Initialize this executor with the relevan function pointer to
     *   extract from the provided signature.
     *
     *   Params:
     *      string signature: the signature to be fuzzed
     *      vector libraries: vector of strings containing path to the .so
     *                        files.
     */
    Executor();

    /**
     * Generate the input for the native method to execute.
     * 
     * This method should return a vecotor of vector of bytes.
     * Each vector in the vector is a test case input
     */
    virtual std::vector<std::vector<char>> generateInput() = 0;

    /**
     * Read the inputs from a fuzzer and returns
     * them in a char* buffer
     *
     * Return:
     *   char* buff -> the input read
     **/
    virtual char* readFuzzerInput() = 0;

    /**
     * Check if there was a crash in the execution.
     */
    virtual bool hasCrashed(std::string output_file) = 0;

    /**
     * execute the function pointer provided with the the input read from the
     * fuzzer see @readFuzzerInput
     */
    virtual bool execute(JNINativeMethod method,
                         std::vector<std::string> parameter_types,
                         char* input) = 0;

    /**
     * Start the executor
     */
    void run(std::string& signature, std::vector<std::string>& libraries);

    JNINativeMethod& getMethodToExecute();
    std::vector<std::string>& getParameters();

};
}  // namespace executor

#endif