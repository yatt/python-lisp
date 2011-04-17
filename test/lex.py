# coding: utf-8
# トークナイザのテスト

import sys
import os
sys.path += os.path.join(os.path.dirname(__file__), "../")

import lisp

def lextest():
    lex = lisp.Lexer()
    f = lambda inputs: lex.tokenize(inputs)
    lst = [
            "1",
            "1.0",
            "0.1",
            '"hello"',
            "#t",
            "#f",
            "+",
            "(+ 1 (+ 2 3))",
            ' \t \n  \r (add "string" #t #f literal 1 1.2 + * ) ',
            '(map fun (list 1 2 3 4 5))',
            '(if [= 3 3] [+ 1 2] [* 1 2])',
            "member?",
            "(1)",
            "(1 . 2)",
            "'()",
            "'(1 2)",
            "'x",
            "**env**",
            "2.3 ; hogehog",
            "+1",
            "-1",
            "+1.0",
            "-1.0",
            "x10",
            "[]",
            "[1 2 [3]]",
        ]
    for n in lst:
        for t in lex.tokenize(n):
            print t
        print "\n"


if __name__ == '__main__':
    lextest()
