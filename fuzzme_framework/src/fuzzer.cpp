#include "fuzzer.h"
#include <stdio.h>
#include <fstream>
#include <sstream>
#include <string>
#include "function_ptrs.h"
#include "jni_extractor.h"
#include "jni_type_mocks.h"
#include "jnienv_mokcs.h"
#include "soot_parser.h"

using namespace jnif;
using namespace extr_jni;
using namespace sootp;

bool isDoubleSignature(std::vector<std::string> param_types, std::string ret_type){
    if(ret_type.compare("double")) {
        return false;
    }

    for(int i=0; i<param_types.size(); i++) {
        std::string param = param_types[i];
        if(param.compare("double")){
            return false;
        }
    }

    return true;
}

JniFuzzer::JniFuzzer(){};

void JniFuzzer::FuzzOne(std::string signature,
                        std::vector<std::string> libraries, int param_index) {
    // 1. extract JNINativeMethod

    DynamicExtractor dynamic_extractor(libraries, "");
    StaticExtractor static_extractor(libraries, "");

    JNINativeMethod method;

    if (!static_extractor.Extract(signature, method)) {
        if (!dynamic_extractor.Extract(signature, method)) {
            LOG_ERR("Couldn't extract %s", signature.c_str());
            throw "Couldn't extract the provided signature";
        }
    }

    // 2 create parameter for the function to be called
    SootParser soot_parser;
    soot_parser.Parse(signature);

    std::vector<std::string> parameter_types = soot_parser.GetParameterTypes();

    void* parameters[parameter_types.size()];
    double doubleParams[parameter_types.size()];

    // Parsing stdin to get input from afl
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

    bool crashed = false;
    {   
        // Checking if there was any crash n the previous run
        std::ifstream infile("tmp.txt");
        std::string line;
        while (std::getline(infile, line)) {
            if(line.back() != ']'){
                crashed = true;
            }
        }
    }

    FILE* out = fopen("/data/local/tmp/workspace/io.txt", "a");
    if (out == NULL) {
        throw "couldn't open input file";
    }

    if(crashed){
        fprintf(out, ", crash]\n");
    }

    // In tmp we store the last i/o log. It is useful in case a crash occured
    FILE* tmp = fopen("/data/local/tmp/workspace/tmp.txt", "w");
    if (tmp == NULL) {
        throw "couldn't open input file";
    }

    std::string message;
    fprintf(out, "[%d, ", param_index);
    fprintf(tmp, "[%d, ", param_index);
    fflush(out);
    fflush(tmp);

    for (int i = 0; i < parameter_types.size(); i++) {
        std::string param_type = parameter_types[i];
        if (i == param_index) {
            // here we want to use the fuzzer input!
            LOG_DEBUG("Fuzzing arg %d", i);
            
            if(isDoubleSignature(parameter_types, soot_parser.GetReturnType())) {
                doubleParams[i] = tmocks::ConvertDoubleFuzzerInput(param_type, buf);
            } else {
                parameters[i] = tmocks::ConvertFuzzerInput(param_type, buf);
            }
        } else if (param_index < parameter_types.size()) {
            // we fix the valueof the other parameters
            if(isDoubleSignature(parameter_types, soot_parser.GetReturnType())) {
                LOG_DEBUG("Setting other arg to 0");
                doubleParams[i] = 0;
            } else {
                char* p = "0";
                LOG_DEBUG("Setting other arg to 0");
                parameters[i] = tmocks::ConvertFuzzerInput(param_type, p);
            }


        } else {
            // we want her to randomly generate inputs for both params at the
            // same time

            LOG_DEBUG("Getting next args");
            void* param = this->GetNextArg(&buf);
            if(isDoubleSignature(parameter_types, soot_parser.GetReturnType())) {
                doubleParams[i] = tmocks::ConvertDoubleFuzzerInput(param_type, (char*)param);
            } else {
                parameters[i] = tmocks::ConvertFuzzerInput(param_type, param);
            }
        }

        // We then log the parameters
        if (i == parameter_types.size() - 1) {
            // this is just for integer purpose
            if(isDoubleSignature(parameter_types, soot_parser.GetReturnType())) {
                fprintf(out, "%f", doubleParams[i]);
                fprintf(tmp, "%f", doubleParams[i]);
                fflush(out);
                fflush(tmp);
            } else {
                fprintf(out, "%d", parameters[i]);
                fprintf(tmp, "%d", parameters[i]);
                fflush(out);
                fflush(tmp);
            }
        } else {
            if(isDoubleSignature(parameter_types, soot_parser.GetReturnType())){
                fprintf(out, "%f, ", doubleParams[i]);
                fprintf(tmp, "%f, ", doubleParams[i]);
                fflush(out);
                fflush(tmp);
            } else {
                fprintf(out, "%d, ", parameters[i]);
                fprintf(tmp, "%d, ", parameters[i]);
                fflush(out);
                fflush(tmp);
            }
        }
    }
    LOG_DEBUG("Input have been properly generated")
    // 3. Create mock JNIEnv
    JNIEnv* env;
    emock::GetMockedEnvironment(&env);

    // 4. call the function
    LOG_DEBUG("Calling function from env...");

    if(isDoubleSignature(parameter_types, soot_parser.GetReturnType())) {
        double retValue = CallDouble(parameter_types.size(), method.fnPtr, env, NULL, doubleParams);
            
        LOG_DEBUG("we just mocked the environment: %f", retValue);

        // We successfully executed the function so let's log the all output

        fprintf(out, ", %f]\n", retValue);
        fprintf(tmp, ", %f]\n", retValue);
        fflush(out);
        fflush(tmp);
        fclose(tmp);
        fclose(out);
    } else {
        void* retValue =
            call(parameter_types.size(), method.fnPtr, env, NULL, parameters);
                // tmocks::JString* my_str = (tmocks::JString*)retValue;
        LOG_DEBUG("we just mocked the environment: %d", retValue);

        // We successfully executed the function so let's log the all output

        fprintf(out, ", %d]\n", retValue);
        fprintf(tmp, ", %d]\n", retValue);
        fflush(out);
        fflush(tmp);
        fclose(tmp);
        fclose(out);
    }


};

// Implementing private methods

void* JniFuzzer::GetNextArg(char** current) {
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