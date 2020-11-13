#include "simple_executor.h"
#include "function_ptrs.h"
#include "jni_type_mocks.h"
#include "jnienv_mokcs.h"
#include "soot_parser.h"

using namespace simple_executor;
using namespace sootp;

SimpleExecutor::SimpleExecutor() : Executor::Executor(){};

std::vector<std::vector<char>> SimpleExecutor::generateInput() {
    vector<vector<char>> vec;
    return vec;
}

char* SimpleExecutor::readFuzzerInput() {
    int chunk_sinze = 4096;
    char* buf = (char*)malloc(chunk_sinze);
    int next_byte = 0, current_char;

    while ((current_char = fgetc(stdin)) != EOF) {
        buf[next_byte++] = (char)current_char;
        buf[next_byte] = '\0';
        if (next_byte >= chunk_sinze - 1) {
            buf = (char*)realloc(buf, chunk_sinze + chunk_sinze);
            chunk_sinze += chunk_sinze;
        }
    }

    return buf;
}

bool SimpleExecutor::execute(JNINativeMethod method,
                             std::vector<std::string> parameter_types,
                             char* input) {
    void* parameters[parameter_types.size()];
    double doubleParams[parameter_types.size()];

    FILE* out = fopen("/data/local/tmp/workspace/io.txt", "a");
    if (out == NULL) {
        throw "couldn't open input file";
    }

    fprintf(out, "\ncrashed");
    fflush(out);
    // convert inputs
    for (int i = 0; i < parameter_types.size(); i++) {
        std::string param_type = parameter_types[i];
        void* param = SimpleExecutor::GetNextArg(&input);
        parameters[i] = tmocks::ConvertFuzzerInput(param_type, param);
        // TODO (clod) file loggig crashes
    }

    JNIEnv* env;
    emock::GetMockedEnvironment(&env);
    
    
    void* retValue =
        call(parameter_types.size(), method.fnPtr, env, NULL, parameters);
    
    fprintf(out, " [no]\n");
    fflush(out);
    fclose(out);
    return true;
}

bool SimpleExecutor::hasCrashed(std::string output_file) { 
    return false;
}

// Private Methods

void* SimpleExecutor::GetNextArg(char** current) {
    // Basically we try to split the input on the
    // special char '0x07'.
    //
    // current points to the end of the last parsed
    // parameter. We go until we find the char 0x07
    // and there we insert a terminator. Current now
    // points one after the terminator and start is the
    // beginning of the argument we are returning
    char* start = *current;

    for (; **current && **current != 7; *current += 1) {
    }

    if (**current == 7) {
        **current = 0;  // add terminator
        *current += 1;
    }

    return start;
}