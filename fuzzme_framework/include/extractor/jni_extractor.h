#ifndef _JNI_EXTRACTOR_H
#define _JNI_EXTRACTOR_H

#include <jni.h>
#include <memory>
#include <string>
#include <vector>
#include "libutils/libutils.h"
#include "signature_parser/signature_parser.h"

namespace extr_jni {

// Extractor Class
// This is the base abstract class used to implement different
// strategy of extraction.
class Extractor {
   public:
    // This enumerate all the signature style we support.
    // Depending on it, the static extractor would behave differently.
    enum SignatureStyle {
        SOOT,
        SMALI,
    };

    Extractor(std::vector<std::string> &library_paths,
              std::string signatures_path);

    Extractor(std::vector<std::string> &library_paths,
              std::string signatures_path, SignatureStyle style);

    // Given a signature, it extract/create the correspective JNINativeMethod
    // into result. result will contain both the name, signature and funcptr to
    // the method in the shared library. Signature will be in the "smali" format
    // unless differnlty specified.
    //
    // All the libraries specified in library_path when creating this object
    // will be considered.
    //
    // Param:
    //      std::string signature -> string representing the signature of the
    //      method to extract. JNINativeMethod& result -> if a method was found,
    //      it will be stored in result
    // Return:
    //      true if a method was successfully found
    virtual bool Extract(std::string signature, JNINativeMethod &result);
    std::vector<std::string> &GetLibraryPaths();

    // Extract the method name given a signature. It works differently depending
    // on the SignatureStyle this Extractor was initialized with.
    //
    // For example given SOOT style and the signature
    // '<org.apache.http.util.EntityUtils: java.lang.String
    // toString(org.apache.http.HttpEntity)>', the expected result is
    // 'toString'.
    //
    // Param:
    //      std::string signature -> the signature from where extracting the
    //      method name
    // Return:
    //      std::string -> return the name of the signature or an empty string
    //      if nothing is found
    // Throw:
    //      sigp::ParseException -> thrown if signature is invalid
    const std::string GetNameFromSignature(std::string signature);

    // Add a library path to the vector.
    // Param:
    //      library_path -> path to be added
    // Return:
    //      void
    void AddLibraryPath(std::string &library_path);

    // This method returns a breakdown of an Android method signature.
    // Currently only soot signature is supported, but in future implementations
    // also smali will be.
    // The breakdown is returned as a tuple object containing:
    //      <method_package, return_type, method_name, [parm1, param2, ...
    //      paramN]>
    // In case the method has no parameter, the parameter array will simply be
    // empty.
    //
    // Param:
    //      std::string signature -> string representing the method signature
    //
    // Return:
    //      std::tuple<const char *, const char *, const char *, const char *[]>
    //      containing the breakdown of the signature
    const std::tuple<const char *, const char *, const char *, const char *[]>
    GetSignatureBreakDown(std::string signature);

    // This method returns the signature style this extractor has been set with
    //
    // Param: void
    // Return:
    //      SignatureStyle style -> the signature style of this extractor
    SignatureStyle &GetSignatureStyle();

    std::shared_ptr<sigp::SignatureParser> GetParser();

   private:
    std::vector<std::string> library_paths_;
    std::string signatures_path_;
    SignatureStyle style_;
    const std::string ExtractNameFromSoot(std::string signature);
    const std::string ExtractNameFromSmali(std::string signature);
    std::vector<std::string> split(std::string strToSplit, char delimeter);
    std::shared_ptr<sigp::SignatureParser> parser_;
};

class DynamicExtractor : public Extractor {
   public:
    DynamicExtractor(std::vector<std::string> &library_paths,
                     std::string signatures_path);
    DynamicExtractor(std::vector<std::string> &library_paths,
                     std::string signatures_path, SignatureStyle style);
    bool Extract(std::string signature, JNINativeMethod &result);

   private:
    void ExtractJni(const char *lib_path);
};

class StaticExtractor : public Extractor {
   public:
    StaticExtractor(std::vector<std::string> &library_paths,
                    std::string signatures_path);
    StaticExtractor(std::vector<std::string> &library_paths,
                    std::string signatures_path, SignatureStyle style);
    bool Extract(std::string signature, JNINativeMethod &result);

    /**
     * Given a signature, it converts it to the partial C like
     * signature, as it appears in the shared library.
     *
     * For example:
     *  <uk.ac.rhul.clod.samplejniapp.MainActivity: java.lang.String
     * fuzzMe(java.lang.string)> becomes
     *  Java_uk_ac_rhul_clod_samplejniapp_MainActivity_fuzzMe
     * Notice that the signature is partial as no parameters are specified here.
     *
     * Param:
     *  std::string the signature to convert
     * Return:
     *  std::string the converted clike signature
     */
    std::string GetCLikeFullName(std::string siganture);

   private:
    // Given a jni method name in the `Java_com_example_MainActivity_test", this
    // method returns true if it finds it in the provided library.
    bool IsMethodStatic(std::string jni_method_name,
                        libutils::LibUtils &lib_utils);
};

}  // namespace extr_jni

#endif