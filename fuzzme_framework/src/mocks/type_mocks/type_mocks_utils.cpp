#include <string>
#include "jni_type_mocks.h"
#include "logging.h"

void* tmocks::ConvertFuzzerInput(std::string type, void* real_input) {
    if (!type.compare("java.lang.String")) {
        tmocks::JString* mock_str = new JString((char*)real_input);
        return mock_str;
    } else if (!type.compare("int") || !type.compare("long") ||
               !type.compare("float")) {
        return (void*)atoi((char*)real_input);
    } else {
        LOG_ERR("not supported type");
        throw "not supported type";
    }
}

double tmocks::ConvertDoubleFuzzerInput(std::string type, char* real_input) {
    return atof(real_input);
}
