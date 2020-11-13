#ifndef _FUZZER_H
#define _FUZZER_H

#include <string>
#include <vector>

namespace jnif {
class JniFuzzer {
   public:
    JniFuzzer();

    /**
     * This method will generate the test environment for the fuzzer.
     * In other words, it extracts the function to be fuzzed and
     * calls it, providing inputs from the one given by the fuzzer.
     * 
     * We fuzz parameter by parameter depending on `param_index`.
     * If a worng index is provided, the program is aborted.
     *
     * Params:
     *      string signature: the signature to be fuzzed
     *      vector libraries: vector of strings containing path to the .so
     *                        files.
     *      int param_index: index of the parameter to be fuzzed
     */
    void FuzzOne(std::string signature, std::vector<std::string> libraries, int param_index);

   private:
    void* GetNextArg(char** current);
};
}  // namespace jnif

#endif