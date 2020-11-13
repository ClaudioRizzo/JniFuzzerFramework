#include <jni.h>
#include <fstream>
#include <string>
#include <vector>
#include "logging.h"
#include <sstream>
#include <iostream>

#include "simple_executor.h"


using namespace std;
using namespace simple_executor;

typedef jstring (*exec_me_ptr)(JNIEnv *, jobject, jstring);

int main(int argc, char const *argv[]) {
    vector<string> libraries_paths;
    vector<string> signatures;
    std::ifstream libs_path_file("libraries.txt");
    std::ifstream signatures_path_file("signatures.txt");
    std::ifstream param_num_path_file("parameter");
    
    std::string lib_path;
    while (std::getline(libs_path_file, lib_path)) {
        libraries_paths.push_back(lib_path);
    }

    std::string signature;
    while (std::getline(signatures_path_file, signature)) {
        signatures.push_back(signature);
    }

    std::string parameter;
    int param_index = 0;
    while (std::getline(param_num_path_file, parameter)) {
        param_index = atoi(parameter.c_str());
    }

    
    Executor *executor;
    SimpleExecutor simple_executor;
    
    executor = &simple_executor;
    if(signatures.size() > 0){
        
        LOG_FILE_DEBUG("========== START FUZZING ==========");
        executor->run(signatures[0], libraries_paths/*param_index*/);
        LOG_FILE_DEBUG("========== END FUZZING ==========");
    }
    
}
