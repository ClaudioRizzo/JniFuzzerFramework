#ifndef _SIMPLE_EXECUTOR_H
#define _SIMPLE_EXECUTOR_H

#include "executor.h"
#include "string"
#include "vector"

namespace simple_executor {

using namespace executor;

class SimpleExecutor : public Executor {
   public:
    SimpleExecutor();

    std::vector<std::vector<char>> generateInput();
    char* readFuzzerInput();
    bool hasCrashed(std::string output_file);
    bool execute(JNINativeMethod method,
                 std::vector<std::string> parameter_types, char* input);
    static void* GetNextArg(char** current);

   private:
    bool crashed = false;
};

};  // namespace simple_executor

#endif