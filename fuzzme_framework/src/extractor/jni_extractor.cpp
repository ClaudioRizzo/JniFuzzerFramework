#include "extractor/jni_extractor.h"
#include <logging.h>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "signature_parser/soot_parser/soot_parser.h"

using namespace extr_jni;

// Extractor Implementation

Extractor::Extractor(std::vector<std::string> &library_paths,
                     std::string signatures_path,
                     Extractor::SignatureStyle style) {
    this->library_paths_ = library_paths;
    this->signatures_path_ = signatures_path;
    this->style_ = style;
    if(this->style_ == SignatureStyle::SOOT){
        this->parser_ = shared_ptr<sootp::SootParser>(new sootp::SootParser());
    } else {
        LOG_DEBUG("not implemented");
        throw "Not implemented style";
    }
}

Extractor::Extractor(std::vector<std::string> &library_paths,
                     std::string signatures_path)
    : Extractor(library_paths, signatures_path, SignatureStyle::SOOT) {
        this->parser_ = shared_ptr<sootp::SootParser>(new sootp::SootParser());
    }

// returns a reference to a vector of library paths
std::vector<std::string> &Extractor::GetLibraryPaths() {
    return this->library_paths_;
}

void Extractor::AddLibraryPath(std::string &library_path) {
    this->library_paths_.push_back(library_path);
}

Extractor::SignatureStyle &Extractor::GetSignatureStyle() {
    return this->style_;
}

const std::string Extractor::GetNameFromSignature(std::string signature) {
    if (this->style_ == SignatureStyle::SOOT) {
        return this->ExtractNameFromSoot(signature);
    } else {
        return this->ExtractNameFromSmali(signature);
    }
}

std::shared_ptr<sigp::SignatureParser> Extractor::GetParser() {
    return this->parser_;
}
/* Start of private methods implementation */

const std::string Extractor::ExtractNameFromSoot(std::string signature) {
    sootp::SootParser soot_parser = sootp::SootParser(signature);
    soot_parser.Parse();
    
    return soot_parser.GetMethodName();
}

std::vector<std::string> Extractor::split(std::string strToSplit,
                                          char delimeter) {
    std::stringstream ss(strToSplit);
    std::string item;
    std::vector<std::string> splittedStrings;
    while (std::getline(ss, item, delimeter)) {
        splittedStrings.push_back(item);
    }
    return splittedStrings;
}

const std::string Extractor::ExtractNameFromSmali(std::string signature) {
    LOG_ERR("We still do not support smali signatures")
    throw "smali is not supported yet";
}

bool Extractor::Extract(std::string signature, JNINativeMethod &result) {
    throw "Method has to be implemented!";
}