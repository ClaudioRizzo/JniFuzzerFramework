#include <fstream>
#include <sstream>
#include <string>
#include "gtest/gtest.h"
#include "soot_parser/soot_parser.h"

namespace {
class SootParserTests : public ::testing::Test {
   public:
    SootParserTests(){};
    std::vector<std::string> GetSignatures() { return this->lines; }

    void SetUp() { this->GetLines(); };
    void TearDown(){};

   private:
    std::ifstream signature_file_;
    std::vector<std::string> lines;

    std::vector<std::string> &GetLines() {
        this->signature_file_.open("soot_parser_test_files/signatures.txt");
        std::string line;
        while (std::getline(this->signature_file_, line)) {
            this->lines.push_back(line);
        }
        return lines;
    }
};

/**
 * This test checks wheter the parser internal counter correctly
 * increases when asking for new tokens. We test it against
 * many signaturtes and check that it is correct for each of them.
 *
 * We also check that the last token is the terminator.
 */
TEST_F(SootParserTests, NextTokenIsValidTest) {
    vector<std::string> signatures = this->GetSignatures();
    for (int j = 0; j < signatures.size(); j++) {
        std::string signature = signatures[j];
        sootp::SootParser sp(signature);

        vector<Token> tokens = sp.GetTokens();
        for (int i = 0; i < tokens.size(); i++) {
            EXPECT_EQ(i, sp.GetTokenIndex());

            if (i == tokens.size() - 1) {
                EXPECT_TRUE(sp.IsTerminator(sp.NextToken()));
            } else {
                sp.NextToken();
            }
        }
    }
};

/**
 * We have a bunch of valid signatures, we should be able to parse
 * all of them without errors
 */
TEST_F(SootParserTests, ParseNoFail) {
    vector<std::string> signatures = this->GetSignatures();
    for (int j = 0; j < signatures.size(); j++) {
        std::string signature = signatures[j];
        sootp::SootParser sp(signature);
        LOG_DEBUG("trying %s", signature.c_str());
        EXPECT_TRUE(sp.Parse());
        LOG_DEBUG("===== DONE ====");
    }
}

/**
 * Given a set of signature to parse, this test
 * checks wheter the parser extracts properly the various
 * component of the signature for a no parameter signature
 */
TEST_F(SootParserTests, ParsePopulateNoParamTest) {
    std::string signature(
        "<android.net.wifi.WifiInfo: java.lang.String getMacAddress()>");
    sootp::SootParser sp(signature);
    sp.Parse();
    EXPECT_FALSE(strcmp(sp.GetPackageName().c_str(), "android.net.wifi.WifiInfo"));
    EXPECT_FALSE(strcmp(sp.GetMethodName().c_str(), "getMacAddress"));
    EXPECT_FALSE(strcmp(sp.GetReturnType().c_str(), "java.lang.String"));
    EXPECT_EQ(sp.GetParameterTypes().size(), 0);

}

/**
 * Given a set of signature to parse, this test
 * checks wheter the parser extracts properly the various
 * component of the signature for a single parameter signature
 */
TEST_F(SootParserTests, ParsePopulateOneParamTest) {
    std::string signature(
        "<android.os.Bundle: java.util.ArrayList "
        "getStringArrayList(java.lang.String)>");
    sootp::SootParser sp(signature);
    sp.Parse();
    
    EXPECT_FALSE(strcmp(sp.GetPackageName().c_str(), "android.os.Bundle"));
    EXPECT_FALSE(strcmp(sp.GetMethodName().c_str(), "getStringArrayList"));
    EXPECT_FALSE(strcmp(sp.GetReturnType().c_str(), "java.util.ArrayList"));
    EXPECT_EQ(sp.GetParameterTypes().size(), 1);
    EXPECT_FALSE(strcmp(sp.GetParameterTypes()[0].c_str(), "java.lang.String"));

}

/**
 * Given a set of signature to parse, this test
 * checks wheter the parser extracts properly the various
 * component of the signature for a multiple parameter signature
 */
TEST_F(SootParserTests, ParsePopulateMultiParamTest) {
    std::string signature(
        "<android.database.sqlite.SQLiteDatabase: android.database.Cursor "
        "query(android.net.Uri,java.lang.String[],java.lang.String,java.lang."
        "String[],java.lang.String)>");
    sootp::SootParser sp(signature);
    sp.Parse();
    
    EXPECT_FALSE(strcmp(sp.GetPackageName().c_str(), "android.database.sqlite.SQLiteDatabase"));
    EXPECT_FALSE(strcmp(sp.GetMethodName().c_str(), "query"));
    EXPECT_FALSE(strcmp(sp.GetReturnType().c_str(), "android.database.Cursor"));
    EXPECT_EQ(sp.GetParameterTypes().size(), 5);
    EXPECT_FALSE(strcmp(sp.GetParameterTypes()[0].c_str(), "android.net.Uri"));
    EXPECT_FALSE(strcmp(sp.GetParameterTypes()[1].c_str(), "java.lang.String[]"));
    EXPECT_FALSE(strcmp(sp.GetParameterTypes()[2].c_str(), "java.lang.String"));
    EXPECT_FALSE(strcmp(sp.GetParameterTypes()[3].c_str(), "java.lang.String[]"));
    EXPECT_FALSE(strcmp(sp.GetParameterTypes()[4].c_str(), "java.lang.String"));

}

/**
 * Test wether the parser properly fails in some cases
 */
TEST_F(SootParserTests, ParseFailAsExpectedTest){
    std::string signature1(
        "<android.database.sqlite.SQLiteDatabase:android.database.Cursor "
        "query(android.net.Uri,java.lang.String[],java.lang.String,java.lang."
        "String[],java.lang.String)>");
    sootp::SootParser sp1(signature1);
    EXPECT_THROW(sp1.Parse(), sigp::ParseException);

    std::string signature2(
        "<android.database.sqlite.SQLiteDatabase: android.database.Cursor "
        "query(android.net.Uri,java.lang.String[] java.lang.String,java.lang."
        "String[],java.lang.String)>");
    sootp::SootParser sp2(signature2);
    EXPECT_THROW(sp2.Parse(), sigp::ParseException);
}

TEST_F(SootParserTests, ParseFromSignatureTest){
    vector<std::string> signatures = this->GetSignatures();
    sootp::SootParser sp;
    for (int j = 0; j < signatures.size(); j++) {
        std::string signature = signatures[j];
        LOG_DEBUG("trying %s", signature.c_str());
        EXPECT_TRUE(sp.Parse(signature));
        LOG_DEBUG("===== DONE ====");
    }
}


}  // namespace