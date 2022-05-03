"""
Simple Interpreter - Part 3
https://ruslanspivak.com/lsbasi-part1/
with additional modifications by Brian Borowski
1) More specific error messages
2) Handles floats as well as ints
3) Allows the user to type 'exit' to end the program
"""
# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, FLOAT, PLUS, MINUS, EOF = 'INTEGER', 'FLOAT', 'PLUS', 'MINUS', 'EOF'


class Token(object):
    def __init__(self, token_type, value):
        # token token_type: INTEGER, PLUS, MINUS, or EOF
        self.type = token_type
        # token value: non-negative integer value, '+', '-', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3 + 5", "12 - 5 + 3", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    ##########################################################
    # Lexer code                                             #
    ##########################################################
    def error(self, msg=None):
        if msg != None:
            raise Exception(msg)
        if self.pos > len(self.text) - 1:
            raise Exception('Unexpected end of file at position %d.' %
                            self.pos)
        raise Exception('Unexpected character \'%c\' at position %d.' %
                        (self.text[self.pos], self.pos))

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        is_int = True
        result = ''
        starting_pos = self.pos
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            is_int = False
            result += self.current_char
            self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if result == '.':
            self.error('Expected numeric value at position {pos:d}, received \'.\''.format(pos=starting_pos))
        return Token(INTEGER, int(result)) if is_int else Token(FLOAT, float(result))
        
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    ##########################################################
    # Parser / Interpreter code                              #
    ##########################################################
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        """Return a numeric(INTEGER or FLOAT) token value."""
        token = self.current_token
        self.eat(token.type)
        return token.value

    def expr(self):
        """Arithmetic expression parser / interpreter."""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        if self.current_token.type not in (INTEGER, FLOAT):
            self.error('Expected numeric value at position 0.')

        starting_pos = self.pos
        result = self.term()
        if self.current_token.type not in (PLUS, MINUS, EOF):
            self.error('Expected operator at position {pos:d}.'.format(pos=starting_pos))
        while self.current_token.type in (PLUS, MINUS):
            starting_pos = self.pos
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                if self.current_token.type in (INTEGER, FLOAT):
                    result = result + self.term()
                else:
                    self.error('Expected numeric value at position {pos:d}.'.format(pos=starting_pos))
            elif token.type == MINUS:
                self.eat(MINUS)
                if self.current_token.type in (INTEGER, FLOAT):
                    result = result - self.term()
                else:
                    self.error('Expected numeric value at position {pos:d}.'.format(pos=starting_pos))
            
        return result


def main():
    while True:
        try:
            text = input('calc> ')
            if text == 'exit':
                raise EOFError
        except EOFError:
            # If user types CTRL+D
            print('Bye.')
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        try:
            result = interpreter.expr()
            print(result)
        except Exception as error:
            print('Error:', error)


if __name__ == '__main__':
    main()
