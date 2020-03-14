import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

soa = np.array([[0, 0, 1, 1, -2, 0], [0, 0, 2, 1, 1, 0],
                [0, 0, 3, 2, 1, 0], [0, 0, 4, 0.5, 0.7, 0]])

soa = np.array([[0, 0, 0, 1 , 0, 0]])
soa2 = np.array([[0, 0, 0, 1 , 1, 0]])

X, Y, Z, U, V, W = zip(*soa)
X2, Y2, Z2, U2, V2, W2 = zip(*soa2)
print(X,Y,Z,U,V,W)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.quiver(1,2,3,4,5,6)
ax.quiver(X, Y, Z, U, V, W)
ax.quiver(X2, Y2, Z2, U2, V2, W2)
ax.set_xlim([-1, 0.5])
ax.set_ylim([-1, 1.5])
ax.set_zlim([-1, 8])
plt.show()