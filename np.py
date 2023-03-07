
import numpy as np

X = np.array([])
listX = []

x = np.array([])
list_x = []

for i in range(2):
    np.append(x, 1)
    list_x.append([1, 2, 3, 4])

np.append(X, x, axis=0)
listX.append(list_x)

print(X)
print(listX)