(define (sum n acc)
    (if (= n 0)
        acc
        (sum (- n 1) (+ n acc))))

(define (pow10 n)
    (if (= n 0)
        1
        (* 10 (pow10 (- n 1)))))

(define (report first last)
    (if (= first last)
        0
        (begin
            (define n (pow10 first))
            (display (list first n (sum n 0)))
            (report (+ first 1) last))))

(display (quote (This takes > 30s to run)))
(report 1 7)
