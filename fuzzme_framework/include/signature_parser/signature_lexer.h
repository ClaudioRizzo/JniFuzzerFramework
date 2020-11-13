#ifndef _SIGNATURE_LEXER_H
#define _SIGNATURE_LEXER_H

#include <stdexcept>
#include <string>
#include <vector>
#include "logging.h"

using namespace std;

namespace sigl {

class Token {
   private:
    int id_;
    string value;

   public:
    Token(){};
    Token(int id, string value) {
        this->id_ = id;
        this->value = value;
    };
    int GetID() { return this->id_; };
    string GetValue() { return this->value; };
};

/**
 * This class is used as a template for a specific lexer (tokenizer).
 * T is a class representing a token that has to be implemented by
 * the lexer using this template.
 */
class SignatureLexer {
   public:
    SignatureLexer(){};
    virtual vector<Token> lex(string signature) = 0;
};

class LexException : std::exception {
 public:
  LexException(const char *message) {
      this->message_ = message;
  };
  const char *what() const throw() {
      return this->message_;
  }

 private:
  const char *message_;
};

}  // namespace sigl

#endif