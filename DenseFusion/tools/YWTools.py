import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import threading
import time

def get_bbox(posecnn_rois,border_list,img_width,img_length,idx):
    rmin = int(posecnn_rois[idx][3]) + 1
    rmax = int(posecnn_rois[idx][5]) - 1
    cmin = int(posecnn_rois[idx][2]) + 1
    cmax = int(posecnn_rois[idx][4]) - 1
    r_b = rmax - rmin
    for tt in range(len(border_list)):
        if r_b > border_list[tt] and r_b < border_list[tt + 1]:
            r_b = border_list[tt + 1]
            break
    c_b = cmax - cmin
    for tt in range(len(border_list)):
        if c_b > border_list[tt] and c_b < border_list[tt + 1]:
            c_b = border_list[tt + 1]
            break
    center = [int((rmin + rmax) / 2), int((cmin + cmax) / 2)]
    rmin = center[0] - int(r_b / 2)
    rmax = center[0] + int(r_b / 2)
    cmin = center[1] - int(c_b / 2)
    cmax = center[1] + int(c_b / 2)
    if rmin < 0:
        delt = -rmin
        rmin = 0
        rmax += delt
    if cmin < 0:
        delt = -cmin
        cmin = 0
        cmax += delt
    if rmax > img_width:
        delt = rmax - img_width
        rmax = img_width
        rmin -= delt
    if cmax > img_length:
        delt = cmax - img_length
        cmax = img_length
        cmin -= delt
    return rmin, rmax, cmin, cmax


#plot line
class plot3dtool(object):
    def __init__(self):
        self.plt=plt
        self.plt.ion()
        self.fig = self.plt.figure(1)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.x=[0]
        self.y=[0]
        self.z=[0]
    def start_show(self):
        show=threading.Thread(target=self.show,args=())
        show.start()
        print("Plot start")
    def show(self):
        # while(1):
        self.ax.plot(self.x, self.y, self.z)
        self.plt.draw()
        self.plt.pause(0.0001)
        self.ax.cla()

    def add(self,xyz):

        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)

#plot operator # deprecated
class plot_operator(object):
    def __init__(self):
        self.p = plot3dtool()
        self.p.show()

    def start(self):
        t=threading.Thread(target=self.keepshowing,args=())
        t.start()
        # t.run()
        print("show, started")
        pass
    def keepshowing(self):
        # while(1):
        print("keepshowing")
        k=0
        while (1):
            print("keepshowing")
            print('1')
            k += 1
            self.p.add([k, k, k])
            # self.p.show()
            time.sleep(1)

#plot vector
class plot3d_vector_tool(object):
    def __init__(self):
        self.plt=plt
        self.plt.ion()
        self.fig = self.plt.figure(1)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.v=[]
    def start_show(self):
        show=threading.Thread(target=self.show,args=())
        show.start()
        print("Plot start")

    def show(self):
        # while(1):
        self.ax.plot(self.x, self.y, self.z)
        self.plt.draw()
        self.plt.pause(0.0001)
        self.ax.cla()

    def add(self,xyz):

        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)


#

#plot 3d vector
class plot3d_vector_tool(object):
    def __init__(self):
        self.plt=plt
        # self.plt.ion()
        self.fig = self.plt.figure("vector plot")
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([0, 2])
        self.vs=[]

    def add_origin(self):
        vs = []
        vs.append([0, 0, 0, 1, 0, 0])
        vs.append([0, 0, 0, 0, 1, 0])
        vs.append([0, 0, 0, 0, 0, 1])
        self.addvs(vs)
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