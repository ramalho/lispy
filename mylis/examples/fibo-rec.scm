{define [fibo n]
    {cond [(= n 0) 0]
          [(= n 1) 1]
          [else (+ (fibo (- n 1))
                   (fibo (- n 2)))]}}

{cond
    [(>= n 20)
     (display (quote (This will take a while)))]}

(display (fibo n))
