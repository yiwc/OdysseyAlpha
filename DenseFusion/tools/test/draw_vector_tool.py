import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

#plot 3d vector
class plot3d_vector_tool(object):
    def __init__(self):
        self.plt=plt
        # self.plt.ion()
        self.fig = self.plt.figure(1)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([0, 2])
        self.vs=[]



    def show(self):
        # while(1):
        for v in self.vs:
            x=[v[0],v[3]]
            y=[v[1],v[4]]
            z=[v[2],v[5]]
            self.ax.quiver(x[0],y[0],z[0],x[1],y[1],z[1])
            # self.ax.plot(self.x, self.y, self.z)
        # self.plt.draw()
        # self.plt.pause(0.0001)
        # self.ax.cla()
        self.plt.show()
    def add(self,v):
        self.vs.append(v)
    def addvs(self,vs):
        for v in vs:
            self.add(v)
if __name__=="__main__":
    p=plot3d_vector_tool()
    vs=[]
    vs.append([0,0,0,1,0,0])
    vs.append([0,0,0,0,1,0])
    vs.append([0,0,0,0,0,1])
    p.addvs(vs)
    p.show()