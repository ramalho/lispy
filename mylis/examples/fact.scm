(define (! n)
    (if (<= n 1)
        1
        (* n (! (- n 1)))))
(display (! x))
