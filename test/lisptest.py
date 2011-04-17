# coding: utf-8

import sys
import os
sys.path += os.path.join(os.path.dirname(__file__), "../")

import lisp

def main():
    lsp = lisp.Lisp(lisp.Lexer(), lisp.Parser(), lisp.Evaluator())
    lst = [
        "(caar '((1 2) (3 4)))",
        "(cadr '((1 2) (3 4)))",
        "(cdar '((1 2) (3 4)))",
        "(cddr '((1 2) (3 4)))",
        "(null? '())",
        "(null? 0)",
        "(zero? 0)",
        "(zero? 3)",
        "(> 1 2)",
        "(> 2 1)",
        "(min 1 6 5 2 -9)",
        "(max 1 6 5 2 -9)",
        "(map (lambda (x) (+ x x)) '(1 2 3 4 5))",
        "(filter even? '(1 2 3 4 5 6))",
        "(abs +1)",
        "(abs -1)",
        "(abs +1.2)",
        "(length '(1 2))",
        "(list-ref '(1 2 3 4 5) 3)",
        "(append '(1 2 3 4) '(5 6 7 8))",
        "(reverse '(1 2 3 4 5))",
        "(sqrt 2.0)",
        #"(map (lambda (n) (expt 2 n)) '(1 2 3 4))",
        "(let ((x 1)) x)",
        "(let ((x 1) (y 2)) (+ x y))",
    ]
    for n in lst:
        result = lsp.evaluator.eval(lsp.parser.parse(lsp.lexer.tokenize(n)))
        print n,"=>",result

if __name__ == '__main__':
    main()
