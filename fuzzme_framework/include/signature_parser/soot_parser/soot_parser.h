#ifndef _SOOT_PARSER_H
#define _SOOT_PARSER_H

#include "signature_parser.h"
#include "soot_lexer.h"
#include "signature_lexer.h"

namespace sootp {
class SootParser : public sigp::SignatureParser {
   public:
    SootParser(string& signature) :
        sigp::SignatureParser(signature, std::shared_ptr<sootl::SootLexer>(new sootl::SootLexer())){}
    SootParser() :
        sigp::SignatureParser(std::shared_ptr<sootl::SootLexer>(new sootl::SootLexer())){}
    bool Parse();
    bool Parse(std::string signature);

    /**
     * Return the next token and increase the token counter by 1.
     * 
     * Return:
     *  Token the next token.
     */
    Token NextToken();

    /**
     * Return the next token but it DOES NOT update the token counter.
     * This method is useful as a look ahead
     * 
     * Return:
     *  Token the next token.
     */
    Token PeekToken();

    /**
     * This method return true if the given token
     * is a terminator one for this parser.
     * 
     * Param: Token token to check wether it's a terminator
     * 
     * Return: True if the token is a terminator
     */
    bool IsTerminator(Token token);

    string GetClikeFullName();


    private:
    string ParseID();
    Token expect(sootl::SootToken::TokenID expected, string error_msg);
    void ParseParameters();
};

}  // namespace sootp

#endif