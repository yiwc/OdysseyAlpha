import numpy as np
# x=np.multiply(my_rotation_matrix_from_euler,np.ndarray([1,0,0,1]).resize([4,1]))
x=np.array([[1,0,0,1]]).transpose()
m=np.array([[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,1]])
res=np.dot(m,x)
# res=np.dot(x,m)
print(res)
pass
