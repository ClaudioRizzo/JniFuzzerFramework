#ifndef _SIGNATURE_PARSER_H
#define _SIGNATURE_PARSER_H

#include <stdexcept>
#include <string>
#include <vector>
#include <memory>

#include "logging.h"
#include "signature_lexer.h"

using namespace std;
using namespace sigl;

namespace sigp {

/**
 * This class is a generic signature parser.
 * To use it, you need to extend it and implement your own
 * parsing logic.
 *
 * Look at SootParser for an example
 */
class SignatureParser {
   public:
    SignatureParser(std::string& signature,
                    std::shared_ptr<SignatureLexer> lexer) {
        this->lexer_ = lexer;
        this->tokens_ = lexer->lex(signature);
    }

    SignatureParser(std::shared_ptr<SignatureLexer> lexer) {
        this->lexer_ = lexer;
    }

    /** This method parses the signature this parser was init with.
     *  If successful, it return true, flase otherwise.
     *  If parsing is successful, this parser is populated
     *  with the extracted value, namely: package name,
     *  return type, method name, function parameters.
     *
     * This method needs to be implemented by This parser
     * subclass, or a logic_exception is thrown
     *
     *
     *  Returns:
     *      bool: true if success, false otherwise
     */
    virtual bool Parse() = 0;

    /** This method parses the provided signature.
     *  If successful, it return true, flase otherwise.
     *  If parsing is successful, this parser is populated
     *  with the extracted value, namely: package name,
     *  return type, method name, function parameters.
     *
     * This method needs to be implemented by This parser
     * subclass, or a logic_exception is thrown
     *
     *  Param:
     *      std::string the signature to parse
     *  Returns:
     *      bool: true if success, false otherwise
     */
    virtual bool Parse(std::string signature) = 0;

    /**
     * This method return the next token if any is present.
     * If no token is left, a symbolic terminator token is
     * returned.
     *
     * The method will increment a local counter which is used as
     * index for the token list. If the counter equals the size
     * of the token list, no more tokens are left and the terminator
     * is returned.
     *
     * Param: N/A
     *
     * Returns:
     *  A token of type Token
     */
    virtual Token NextToken() = 0;
    virtual Token PeekToken() = 0;

    virtual bool IsTerminator(Token token) = 0;

    
    virtual string GetClikeFullName() = 0;
    
    string GetPackageName() { return this->package_name_; };
    void SetPackageName(string package_name) {
        this->package_name_ = package_name;
    }

    string GetReturnType() { return this->return_type_; }
    void SetReturnType(string return_type) { this->return_type_ = return_type; }

    string GetMethodName() { return this->method_name_; }
    void SetMethodName(string method_name) { this->method_name_ = method_name; }

    vector<string> GetParameterTypes() { return this->parameter_types_; }
    void AddParameterType(string& parameter_type) {
        this->parameter_types_.push_back(parameter_type);
    }

    /**
     * Increase the current token index by 1.
     * If the token index reached its maximum value (size of tokens list)
     * then the index won't be incremented and False would be returned.
     *
     * Returns:
     *  true if the index has been incremented, false otherwise
     */
    bool IncreaseTokenIndex() {
        if (this->token_index_ == this->tokens_.size()) {
            return false;
        }
        this->token_index_ += 1;
        return true;
    }

    int GetTokenIndex() { return this->token_index_; }

    vector<Token>& GetTokens() { return this->tokens_; }

    void SetTokens(vector<Token>& tokens) { this->tokens_ = tokens; }

    // Reset the parser to work with another signature
    void ResetParser(std::string signature){
        this->token_index_ = 0;
        this->tokens_ = this->lexer_->lex(signature);
    }

   private:
    vector<Token> tokens_;
    string package_name_;
    string method_name_;
    string return_type_;
    vector<string> parameter_types_;
    int token_index_ = 0;
    std::shared_ptr<SignatureLexer> lexer_;
};

class ParseException : std::exception {
   public:
    ParseException(const char* message) { this->message_ = message; };
    const char* what() const throw() { return this->message_; }

   private:
    const char* message_;
};

}  // namespace sigp

#endif