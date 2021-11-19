(define (! n)
    (factorial-iter n 1))

(define (factorial-iter n product)
    (if (= n 1)
        product
        (factorial-iter (- n 1) (* n product))))
(display (! x))
