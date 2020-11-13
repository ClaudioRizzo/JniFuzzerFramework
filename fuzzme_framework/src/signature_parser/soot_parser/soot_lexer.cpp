#include "soot_lexer.h"
#include <iostream>
#include "logging.h"

using namespace sootl;

// Public methods implementations follow

SootLexer::SootLexer() : SignatureLexer::SignatureLexer() {}

vector<Token> SootLexer::lex(string signature) {
    vector<Token> tokens;
    std::string buff = "";

    int start = 0;
    int end = signature.length();

    if(signature[start] == '<'){
        start+=1;
    }

    if(signature[end-1] == '>'){
        end-=1;
    }

    for (int i = start; i < end; i++) {
        char current_char = signature[i];

        if (current_char == ':') {
            SootToken col_token = SootToken(SootToken::TokenID::COL, ":");
            this->AddToken(col_token, tokens, buff);
        } else if (current_char == ' ') {
            SootToken space_token = SootToken(SootToken::TokenID::SPACE, " ");
            this->AddToken(space_token, tokens, buff);
        } else if (current_char == '(') {
            SootToken lp_token = SootToken(SootToken::TokenID::LP, "(");
            this->AddToken(lp_token, tokens, buff);
        } else if (current_char == ')') {
            SootToken rp_token = SootToken(SootToken::TokenID::RP, ")");
            this->AddToken(rp_token, tokens, buff);
        } else if (current_char == ',') {
            SootToken com_token = SootToken(SootToken::TokenID::COM, ",");
            this->AddToken(com_token, tokens, buff);
        } else {
            buff += current_char;
        }
    }
    tokens.push_back(SootToken(SootToken::TokenID::TERMINATOR, "<end>"));
    return tokens;
}

// Private methods implementation follows
void SootLexer::AddToken(Token& token, vector<Token>& tokens, string& buff) {
    this->TestToken(buff, tokens);
    tokens.push_back(token);
    buff = "";
}

void SootLexer::TestToken(std::string& token_str, vector<Token>& tokens) {
    if (!token_str.compare("")) {
        // it is an empty id which means we had two token close to each other
        // let's just return
        return;
    } else if (this->IsGeneralID(token_str)) {
        tokens.push_back(SootToken(SootToken::TokenID::GEN_ID, token_str));
    } else {
        LOG_DEBUG("invalid token %s", token_str.c_str());
        LOG_ERR("invalid token %s", token_str.c_str());
        string error_message = "invalid token "+token_str;
        throw LexException(error_message.c_str());
    }
}

bool SootLexer::IsGeneralID(std::string general_id) {
    for (int i = 0; i < general_id.length(); i++) {
        char current = general_id[i];
        if (!isprint(current)) {
            return false;
        }
    }
    return true;
}