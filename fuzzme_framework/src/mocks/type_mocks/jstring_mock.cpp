#include "jni_type_mocks.h"
#include "string"
#include "iostream"
#include "logging.h"
#include <cstring>

using namespace tmocks;

JString::JString(char *str)
{
    this->buff_ = str;
    this->size_ = std::strlen(str);
    
}

JString::JString()
{
    this->buff_ = "";
    this->size_ = 0;
    
}

char *JString::getString()
{   
    return this->buff_;
}

int JString::GetSize() {
    return this->size_;
}