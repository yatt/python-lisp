# coding: utf-8

import sys
import os
sys.path += os.path.join(os.path.dirname(__file__), "../")

import lisp

def main():
    l = lisp.Lexer()
    p = lisp.Parser()
    e = lisp.Evaluator()
    lst = ["1", "1.2", '"string"', "(+ 1 2 3)", "(+ 1 (+ 2 3))",
        "(+)",
        "(*)",
        "(cons 1 2)",
        '(cons "apple" "orange")',
        '(cons (cons "apple" 120) (cons "orange" 110))',
        "(car (cons 1 2))",
        "(<)",
        "(< 1)",
        "(< 1 2)",
        "(< 2 1)",
        "(= 1 2)",
        "(= 2 2)",
        "(list 1 2 3 4 5)",
        '(display "Hello, World!")',
        "(lambda (x) (+ x 1))",
        "(eval (+ 3 4))",
        "(quote label)",
        "(quote (cons 1 2))",
        "(define x 1)",
        "(define (inc x) (+ x 1))",
        "(inc 1)",
        "((lambda (x) (+ x 1)) 2)",
        "(if (= #t #t) (+ 1 5) 2)",
        "(apply car '(1 2))",
        "((lambda (x y) (+ x y)) 7 8)",
        "( (lambda (x y) (- x (* (/ x y) y)))  8 3)" # modulo
        "((lambda (x) (+ x x)) 2)",
        "(define (f x y) (+ x y))",
        "f",
        "(f 10 1)",
        "(define (g x y z) (+ x y z))",
        "g",
        "(g 1 2 3)",
        "(let ((x 2)) (+ x x))",
        '(let ((c (read-char))) (if (= c "\n") #t #f))',
        "((lambda () (+ 2 3)))",
        ]
    for i,n in enumerate(lst):
        print "--- no.%d ---" % i
        print n,"=>",
        tree = p.parse(l.tokenize(n))
        print tree,"=>", e.eval(tree)

if __name__ == '__main__':
    main()
