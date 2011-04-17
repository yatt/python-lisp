; startup

(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))
(define (caddr x) (car (cdr (cdr x))))
(define else #t)

(define (not x) (if (eq? x #f) #t #f))

(define (inc x) (+ x 1))
(define (dec x) (- x 1))

(define (member lst x)
  (cond ((null? lst) #f)
    ((eq? x (car lst)) #t)
    (else (member (cdr lst) x))
    )
  )
(define (null? x) (eq? '() x))
(define (zero? x) (eq? x 0))

; map, for-each
(define (map f lst)
  (if (null? lst) '()
      (cons (f (car lst))
        (map f (cdr lst))
        )
      )
  )
(define (for-each f lst)
  (begin
    (map f lst)
    '()
    )
  )
; filter
(define (filter f lst)
  (if (null? lst)
      '()
      (if (eq? #t (f (car lst)))
	  (cons (car lst) (filter f (cdr lst)))
	  (filter f (cdr lst)))
      )
  )

; reduce
; TODO: implement
(define (reduce f lst init)
    (if (null? lst)
        init
        (reduce f (cdr lst) (f init (car lst)))
        )
  )
(define foldr reduce)

; primitive relational operation
(define (>= x y) (not (< x y)))
(define (<= x y) (or (= x y) (< x y)))
(define (> x y) (not (<= x y)))

; max,min
(define (_max2 x y) (if (< x y) y x))
(define (_min2 x y) (if (< x y) x y))
(define (max lst) (foldr _max2 lst))
(define (min lst) (foldr _min2 lst))


; 剰余
(define (modulo x y)
  (- x (* (/ x y) y))
  )
; 偶数、奇数判定
(define (even? x) (eq? (modulo x 2) 0))
(define (odd? x)  (not (even? x)))


;; リスト操作関数群
; list-ref
(define (list-ref xlst index)
  (if (zero? index)
      (car xlst)
      (list-ref (cdr xlst) (- index 1))
      )
  )
; length
(define (length lst)
    (if (null? lst) 0
      (+ 1 (length (cdr lst)))
      )
    )
; append
(define (append x y)
  (if (null? x)
      y
      (cons (car x) (append (cdr x) y))
      )
  )
; reverse
(define (_rev lst ret)
 (if (null? lst)
  ret
  (_rev (cdr lst) (cons (car lst) ret))
  )
 )
(define (reverse lst)
  (_rev lst '())
 )

; sort
; TODO: implement


; range
(define (_range m n)
  (if (= m n)
      '()
      (cons m (_range (+ m 1) n))
      )
  )
(define (range n)
    (_range 0 n)
  )

; abs
(define (abs n)
  (if (< n 0)
      (- 0 n)
      n)
  )

; 2乗根 newton method
(define (_sqrt x a)
  (if (> (abs (- x (* a a))) _eps)
      (_sqrt x (/ (+ a (/ x a)) 2.0))
      a)
  )
(define (sqrt x)
  (if (< x 0) 1.0 (_sqrt x 1.0))
  )

; 対数オーダーのexpの実装
; expt x 0 = 1
; expt x y = if even(y)
;           then expt(x, y/2)^2    [even]
;           else x * expt(x, y-1)  [odd]
(define (expt x y)
  (if (zero? y)
      1
      (if (even? y)
        (let ((z (expt x (/ y 2))))
           (* z z))
        (* x (expt x (- y 1)))
        )
      )
  )


; sin,cos,tan
; 級数展開
; TODO: implement
(define _eps 0.00000000001)
(define (sin x)
    '()
  )
(define (cos rad)
    '()
  )
(define (tan rad)
    (/ (cos rad) (sin rad))
  )


(define (replicate n item)
    (if (zero? n)
        '()
        (cons item (replicate (- n 1)))
        )
    )
(define (id x) x)
