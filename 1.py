import numpy as np

#1
M = np.linspace(2, 26, 25)
print(M)
print('')

#2
M = M.reshape(5,5)
print(M)
print('')

#3
A = np.zeros((3,3))
for y in range(0,3) :
    for x in range(0,3) :
        M[y+1][x+1] = A[y][x]
print(M)
print('')

#4
M = M @ M
print(M)
print('')

#5
B = np.array([1,1,1,1,1])
B.reshape((5,1))
print(np.sqrt((M[0]*M[0]) @ B))
