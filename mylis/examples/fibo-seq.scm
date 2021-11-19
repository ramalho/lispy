(define (fibo-seq n)
    (fibo-seq-iter 1 0 n ()))

(define (fibo-seq-iter a b count seq)
    (if (= count 0)
        (reverse seq)
        (fibo-seq-iter
            (+ a b)
            a
            (decrement count)
            (cons a seq))))

(define (decrement n) (- n 1))

(define (reverse lis)
    (if (null? lis)
        ()
        (append (reverse (cdr lis))
                (list (car lis)))))

(display (fibo-seq n))
