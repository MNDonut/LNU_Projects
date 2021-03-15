import numpy as np
def rotation(m):
    n = len(m)
    for i in range(n-1):
        for j in range(i+1, n):
            c = m[i][i] / (m[i][i]**2 + m[j][i]**2) ** .5
            s = m[j][i] / (m[i][i]**2 + m[j][i]**2) ** .5 
            first = [m[i][k] * c + m[j][k] * s for k in range(len(m[i]))]
            second = [m[i][k] * -s + m[j][k] * c for k in range(len(m[i]))]
            for k in range(len(m[i])):
                m[i][k] = first[k]
                m[j][k] = second[k]

    print("Solved matrix:")
    for row in m:
        print(row)

    for i in range(len(m)):
        if not m[i][i]:
            return "Matrix hasn't solving!"

    x = [0 for i in range(n)]
    for k in range(n - 1, -1, -1):
        x[k] = (m[k][-1] - sum([m[k][j] * x[j] for j in range(k + 1, n)])) / m[k][k]

    return str(x)
            
matrix = np.loadtxt('matrix.txt', usecols=range(5), dtype = int)
print(f"Input matrix:\n{matrix}\n")
print("\nAnswer: " + rotation(matrix))