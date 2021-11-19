(define (member item lst)
    (cond ((null? lst) #f)
          ((equal? item (car lst)) lst)
          (else (member item (cdr lst)))))

(define (member? item lst)
    (and (member item lst) item))

(define small-primes
  (list 5 7 11 13 17 19 23 29 31 37 41 43
        47 53 59 61 67 71 73 79 83 89 97))

(display (member? n small-primes))
