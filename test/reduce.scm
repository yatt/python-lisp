(define add
    (reduce (lambda (x y) (+ x y)) (range 10) 0)
)
(define mul
    (reduce (lambda (x y) (* x y)) (cdr (range 10)) 1)
)
(print add)
(print mul)
