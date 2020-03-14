import numpy as np

a=np.array([[0,1],[2,3]])
print(a)
#[[0 1]
# [2 3]]
a=a.flatten()
print(a)
#[0 1 2 3]
a=a.nonzero()
print(a)
print(a[0])
#(array([1, 2, 3], dtype=int64),)
#[1 2 3]


a=np.array([[0,1,2,3],[2,3,4,5],[4,5,6,7]])
b=a[:,1:2]
print(b) #[[1] ,[3], [5]]