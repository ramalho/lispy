(define (fibo n)
  (fibo-iter 1 0 n))

(define (fibo-iter a b count)
  (if (= count 0)
      b
      (fibo-iter (+ a b) a (- count 1))))

(display (fibo n))
