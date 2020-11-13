#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include "gtest/gtest.h"
#include "extractor/jni_extractor.h"
#include "logging.h"

namespace {
class ExtractorTests : public ::testing::Test {
 private:
  std::ifstream signature_map_file_;
  std::map<std::string, std::string> name_to_signature_map_;
  std::vector<std::string> lines;

  std::vector<std::string> &GetLines() {
    this->signature_map_file_.open("extractor_test_files/signature_map_name.txt");
    std::string line;
    while (std::getline(this->signature_map_file_, line)) {
      this->lines.push_back(line);
    }
    return lines;
  }

  void PopulateMap(){
      int delimiter = 0;
      for(int i=0; i<this->lines.size(); i++){
          std::string line = lines[i];
          delimiter = line.find('|');
          std::string signature = line.substr(0, delimiter-1);
          std::string name = line.substr(delimiter+1, lines.size()-1);
          this->name_to_signature_map_.insert(std::pair<std::string, std::string>(name, signature));
      }
  }

 public:
  void SetUp() {
    this->GetLines();
    this->PopulateMap();
  }

  void TearDown() {
    // code here will be called just after the test completes
    // ok to through exceptions from here if need be
  }

  std::map<std::string, std::string> &GetNameToSigMap() {
    return this->name_to_signature_map_;
  }
};

// Test that we correctly extract all the method names from the given signatures
// Signatures are taken from flowdroid sources file
TEST_F(ExtractorTests, GetNameFromSignatureSootTest) {
    std::map<std::string, std::string> my_map = this->GetNameToSigMap();
    std::vector<std::string> empty_mock;
    extr_jni::Extractor extractor(empty_mock, "", extr_jni::Extractor::SignatureStyle::SOOT);
    
    for (std::map<std::string,std::string>::iterator it=my_map.begin(); it!=my_map.end(); ++it){
        std::string expected = it->first;
        std::string signature = it->second;
        LOG_DEBUG("signature: %s", signature.c_str());
        LOG_DEBUG("expected: %s", expected.c_str());

        std::string extracted = extractor.GetNameFromSignature(signature);
        LOG_DEBUG("extracted: %s", extracted.c_str() );
        ASSERT_EQ(0, strcmp(expected.c_str(), extracted.c_str()));
    }

    }
} // namespace