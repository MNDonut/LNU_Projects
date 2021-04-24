import numpy as np

def SP(A, epsilon):
    yk = np.ones(len(A))
    sk = sum([x * x for x in yk])
    ykNorm = sk ** (1/2)
    xk = yk / ykNorm
    k, lambPrev, lambk = 0, 0, 0
    while True:
        k += 1
        yk = np.dot(A, xk)
        sk = sum([x * x for x in yk])
        tk = sum([x * y for y, x in zip(yk, xk)])
        ykNorm = sk ** (1/2)
        xk = yk / ykNorm
        lambPrev = lambk
        lambk = sk / tk 
        if abs(lambk - lambPrev) <= epsilon:
            print(f"\nIteration: {k}\nLambda: {lambk}")
            break

SP(np.array([[15, 4, 3, 8], [4, 10, 4, 2], [3, 4, 10, 2], [8, 2, 2, 12]]), 0.000000001)
