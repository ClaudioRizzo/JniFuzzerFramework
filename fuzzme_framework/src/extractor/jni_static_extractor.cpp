#include "jni_extractor.h"
#include "libutils/libutils.h"
#include "logging.h"

using namespace extr_jni;

StaticExtractor::StaticExtractor(std::vector<std::string> &library_paths,
                                 std::string signatures_path)
    : Extractor::Extractor(library_paths, signatures_path) {}

StaticExtractor::StaticExtractor(std::vector<std::string> &library_paths,
                                 std::string signatures_path,
                                 SignatureStyle style)
    : Extractor::Extractor(library_paths, signatures_path,
                           SignatureStyle::SOOT) {}

bool StaticExtractor::Extract(std::string signature, JNINativeMethod &result) {
    std::string jni_method_name = this->GetCLikeFullName(signature);
    std::vector<std::string> library_paths = this->GetLibraryPaths();

    for (int i = 0; i < library_paths.size(); i++) {
        std::string lib_path = library_paths[i];
        libutils::LibUtils lib_utils(lib_path.c_str());
        
        if (this->IsMethodStatic(jni_method_name, lib_utils)) {
            // TODO (clod): currently we do not convert the signature field
            // this ends up being not standard among dynamic and static extractor
            // we may need to standardize it.
            result.name = jni_method_name.c_str();
            result.signature = signature.c_str(); // TODO (clod) this has to change
            result.fnPtr = lib_utils.GetFunctionPtr(jni_method_name.c_str());
            LOG_DEBUG("(extractor) function ptr: %x", result.fnPtr);
            LOG_FILE_DEBUG("(extractor) function ptr: %x", result.fnPtr);
            return true;
        }
    }
    return false;
}

bool StaticExtractor::IsMethodStatic(std::string jni_method_name,
                                     libutils::LibUtils &lib_utils) {
    try {
        lib_utils.GetFunctionPtr(jni_method_name.c_str());
        LOG_DEBUG("%s is static", jni_method_name.c_str());
        LOG_FILE_DEBUG("%s is static", jni_method_name.c_str());
        return true;
    } catch (libutils::FunctionPointerLookupException ex) {
        LOG_DEBUG("%s is **NOT** static", jni_method_name.c_str());
        LOG_FILE_DEBUG("%s is **NOT** static", jni_method_name.c_str());
        return false;
    }
}

std::string StaticExtractor::GetCLikeFullName(std::string siganture) {
    this->GetParser()->Parse(siganture);
    return this->GetParser()->GetClikeFullName();
}