#include "soot_parser.h"
#include <algorithm>
#include "logging.h"

using namespace sootp;

Token SootParser::NextToken() {
    Token token = this->GetTokens()[this->GetTokenIndex()];
    this->IncreaseTokenIndex();
    return token;
}

bool SootParser::Parse() {
    vector<Token> tokens = this->GetTokens();

    // package
    string package_name = this->ParseID();
    this->SetPackageName(package_name);

    Token ctoken =
        this->expect(sootl::SootToken::TokenID::COL, "expected ':' found '%s'");

    this->expect(sootl::SootToken::TokenID::SPACE, "expected ' ' found '%s'");

    // return type
    string return_type = this->ParseID();
    this->SetReturnType(return_type);

    this->expect(sootl::SootToken::TokenID::SPACE, "expected ' ' found '%s'");

    // method name
    string method_name = this->ParseID();
    this->SetMethodName(method_name);

    this->expect(sootl::SootToken::TokenID::LP, "expected '(' found '%s'");

    if (this->PeekToken().GetID() == sootl::SootToken::TokenID::GEN_ID) {
        this->ParseParameters();
    }

    this->expect(sootl::SootToken::TokenID::RP, "expected ')' found '%s'");
    this->expect(sootl::SootToken::TokenID::TERMINATOR,
                 "expected terminator found '%s'");

    return true;
}

bool SootParser::Parse(std::string signature) {
    this->ResetParser(signature);
    return this->Parse();
}

bool SootParser::IsTerminator(Token token) {
    return token.GetID() == sootl::SootToken::TokenID::TERMINATOR;
}

string SootParser::GetClikeFullName() {
    std::string full_name =
        "Java_" + this->GetPackageName() + "_" + this->GetMethodName();
    std::replace(full_name.begin(), full_name.end(), '.', '_');
    return full_name;
}

// Start implementing private methods from here

Token SootParser::expect(sootl::SootToken::TokenID expected, string error_msg) {
    Token next = this->NextToken();
    if (next.GetID() != expected) {
        LOG_DEBUG(error_msg.c_str(), next.GetValue().c_str());
        LOG_ERR(error_msg.c_str(), next.GetValue().c_str());
        throw sigp::ParseException(error_msg.c_str());
    }
    return next;
}

string SootParser::ParseID() {
    Token id_token = this->expect(sootl::SootToken::TokenID::GEN_ID,
                                  "expected GEN_ID found '%s'");
    string value = id_token.GetValue();
    for (int i = 0; i < value.size(); i++) {
        char current_char = value[i];
        if (!isascii(current_char)) {
            LOG_DEBUG("non ascii char '%c' found in %s", current_char,
                      value.c_str());
            LOG_ERR("non ascii char '%c' found in %s", current_char,
                    value.c_str());
            throw sigp::ParseException("non ascii char found in id");
        }
    }
    return value;
}

void SootParser::ParseParameters() {
    string first_param_type = this->ParseID();
    this->AddParameterType(first_param_type);

    while (this->PeekToken().GetID() == sootl::SootToken::TokenID::COM) {
        this->expect(sootl::SootToken::TokenID::COM, "");
        string param_type = this->ParseID();
        this->AddParameterType(param_type);
    }
}

Token SootParser::PeekToken() {
    return this->GetTokens()[this->GetTokenIndex()];
}