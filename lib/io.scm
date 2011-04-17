; input
(define (read n)
    (let ((callit (lambda (f) (f))))
        (map callit (replicate n read-char))
        )
    )

(define (read-line)
    (let ((c (read-char)))
        (if (= c "\n")
            '()
            (cons c (read-line))
            )
        )
    )

; output
(define (print x)
    (begin
        (display x)
        (newline)
        )
    )
