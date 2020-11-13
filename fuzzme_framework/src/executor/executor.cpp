#include "executor.h"
#include "jni_extractor.h"
#include "soot_parser.h"

using namespace executor;
using namespace extr_jni;
using namespace sootp;

Executor::Executor(){

};

void Executor::run(std::string& signature,
                   std::vector<std::string>& libraries) {
    DynamicExtractor dynamic_extractor(libraries, "");
    StaticExtractor static_extractor(libraries, "");

    JNINativeMethod method;

    if (!static_extractor.Extract(signature, method)) {
        if (!dynamic_extractor.Extract(signature, method)) {
            LOG_ERR("Couldn't extract %s", signature.c_str());
            throw "Couldn't extract the provided signature";
        }
    }

    SootParser soot_parser;
    soot_parser.Parse(signature);
    std::vector<std::string> parameter_types = soot_parser.GetParameterTypes();
    
    char* buff = readFuzzerInput();
    execute(method, parameter_types, buff);
}
