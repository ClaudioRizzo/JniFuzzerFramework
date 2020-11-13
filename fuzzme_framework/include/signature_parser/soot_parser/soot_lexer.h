#ifndef _SOOT_LEXER_H
#define _SOOT_LEXER_H

#include "signature_lexer.h"

using namespace sigl;

namespace sootl {

/**
 * This is an implementation of the more general Token
 * Class. A soot token is essentially a Token where an
 * enum of tokens has been defined.
 */
class SootToken : public Token {
   public:
    enum TokenID {
        SPACE,   // " "
        LP,      // (
        RP,      // )
        COL,     // :
        COM,     // ,
        GEN_ID,  // general ID
        TERMINATOR,
    };

    SootToken(TokenID id, string value) : Token(id, value) {};
};

/**
 * SootLexer is a specific implementation of SignatureLexer.
 * This lexer is specialized for tokenize soot signatures.
 */
class SootLexer : public SignatureLexer {
   public:
    SootLexer();

    /**
     * Implements lex from SignatureLexer.
     * Given a siganture soot like, this
     * method will return a vector of Tokens.
     * 
     * Param:
     *  std::signature signature to be tokenized
     * Return:
     *  vector<Token> vector of tokens obtained
     */
    vector<Token> lex(string signature);

   private:
    void AddToken(Token& token, vector<Token>& tokens, string& buff);
    void TestToken(std::string& token_str, vector<Token>& tokens);
    bool IsGeneralID(std::string general_id);
};
}  // namespace sootl
#endif