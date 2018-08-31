# -*- Mode: Python -*-

# simple s-expression reader.

import string
import sys
import pprint

all_symbols = {}

def get_symbol (s):
    if all_symbols.has_key (s):
        return all_symbols[s]
    else:
        result = symbol(s)
        all_symbols[s] = result
        return result

class symbol:
    def __init__ (self, s):
        self.s = s
    def __repr__ (self):
        return self.s

class reader:

    def __init__ (self, file):
        self.file = file
        self.char = self.file.read(1)

    def peek (self):
        return self.char

    def next (self):
        result, self.char = self.char, self.file.read(1)
        return result

    def skip_whitespace (self):
        while 1:
            ch = self.peek()
            if not ch:
                break
            elif ch not in string.whitespace:
                # comments?
                if ch == ';':
                    while self.next() not in '\r\n':
                        pass
                else:
                    break
            else:
                self.next()

    def read (self):
        self.skip_whitespace()
        ch = self.peek()
        if not ch:
            raise EOFError ('unexpected end of file')
        elif ch == '(':
            return self.read_list()
        elif ch == '"':
            return self.read_string()
        elif ch in '-0123456789':
            a = self.read_atom()
            if a == '-':
                return '-'
            all_digits = 1
            for ch in a:
                if ch not in '-0123456789':
                    all_digits = 0
                    break
            if all_digits:
                return int (a)
            else:
                return a
        elif ch == '\r':
            if self.read() != '\n':
                raise SyntaxError
            else:
                return
        else:
            return get_symbol (self.read_atom())

    def read_atom (self):
        # read at least one character
        result = [self.next()]
        while 1:
            ch = self.peek()
            if ch == '' or ch in string.whitespace or ch in '()':
                return ''.join (result)
            else:
                result.append (self.next())

    def read_string (self):
        result = []
        ch = self.next()
        while 1:
            ch = self.peek()
            if ch == '"':
                self.next()
                return ''.join (result)
            else:
                result.append (self.next())

    def read_list (self):
        result = []
        paren = self.next()
        while 1:
            self.skip_whitespace()
            p = self.peek()
            if p == ')':
                ch = self.next()
                return result
            else:
                result.append(self.read())

    def read_all (self):
        result = []
        while self.peek() != '':
            result.append (self.read())
            self.skip_whitespace()
        return result

if __name__ == '__main__':
    exps = reader (open (sys.argv[1], 'rb')).read_all()
    for exp in exps:
        pprint.pprint (exp)
