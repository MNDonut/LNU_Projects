import numpy as np
from numpy import linalg as matrix
def conjgrad(A, b, x, e):
    r = b - np.dot(A, x)
    p = r
    k = 0

    while True:
        alpha = (np.dot(np.transpose(r), p)) / (np.dot(np.transpose(p), np.dot(A, p)))
        x = x + np.dot(alpha, p)
        r = r - np.dot(np.dot(alpha, A), p)
        k += 1
        if matrix.norm(r) <= e:
            break
        beta = (np.dot(np.transpose(r), np.dot(A, p))) / (np.dot(np.transpose(p), np.dot(A, p)))
        p = r - np.dot(beta, p)
    print(k)
    return x

a = np.array([[15, -4, -3, 8], 
              [-4, 10, -4, 2], 
              [-3, -4, 10, 2],
              [8, 2, 2, 12]])

print(conjgrad(a, [2, -12, -4, 6], [100, 100, 100, 100], 1e-5))







