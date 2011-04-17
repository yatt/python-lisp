# coding: utf-8

import sys
import os
sys.path += os.path.join(os.path.dirname(__file__), "../")

import lisp

def main():
    p = lisp.Parser()
    lex = lisp.Lexer()
    par = lisp.Parser()
    f = lambda inputs: par.parse(lex.tokenize(inputs))
    lst = ["1", "1.2", "hello", '"hello"', "#t", "#f",
            "(1 . 2)", "(1)", "(0 1 2)",
            "(+ 1 (+ 2 3))",
            "(list 1 2)", "<", "<=", "label?",
            "()",
            "'()",
            "'(1 2 3)",
            "[]",
            "'[]",
            "'[1 2 3]",
            "[(lambda (x) (* x x)) 5]",
            ]
    for n in lst:
        print n,"=>",f(n)
        

if __name__ == '__main__':
    main()
