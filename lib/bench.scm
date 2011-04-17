; bench.scm

; factorial
(define (factorial n)
  (if (zero? n)
      1
      (* n (factorial (- n 1)))
      )
  )
(define (factorial-tailcall n acc)
    (if (zero? n)
        acc
        (factorial-tailcall (- n 1) (* acc n))
        )
    )

; ackermmann
(define (ackermann m n)
  (cond ((zero? m) (+ n 1))
        ((zero? n) (ackermann (- m 1) 1))
        (else      (ackermann (- m 1) (ackermann m (- n 1))))
        )
  )

; hanoi
(define (hanoi n src etc dest)
  (if (zero? (- n 1))
      (list src dest)
      (append (hanoi (- n 1) src dest etc)
              (list src dest)
              (hanoi (- n 1) etc src dest)
              )
      )
  )
  

; tak
(define (tak x y z)
  (if (<= x y)
      y
      (tak (tak (- x 1) y z)
           (tak (- y 1) z x)
           (tak (- z 1) x y)
           )
      )
  )

; lazy tak using quote
