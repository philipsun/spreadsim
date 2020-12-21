# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name: Xiaoping Sun
# Purpose:
# Create Time: 2020/12/18 11:00
# Author: Xiaoping Sun xiaopingsun@gmail.com//971994252@qq.com
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------
import numpy as np
import math
import sxpColorMan
class GeoMap():
    def __init__(self,window=[0,400,0,400],originpt=[0.5,0.5],step=5):
        self.window = window
        self.w = self.window[1]-self.window[0]
        self.h = self.window[3] - self.window[2]
        self.originpt = originpt
        self.all_point = []
        self.current_point = self.mapwindowpt(originpt)
        self.step = step
    def mapcoordy(self,y):

        ny=self.originpt[1] + (self.window[3]-self.originpt[1])*y
        return ny
    def map2window2pt(self,win1pt,window2):
        w = window2[1]-window2[0]
        h = window2[3]-window2[2]
        x = win1pt[0]/self.w*w + window2[0]
        y = win1pt[1]/self.h*h + window2[2]
        return [x,y]
    def mapwindowpt(self,pt):
        npt =pt.copy()
        npt[0]=self.window[0] + (self.window[1]-self.window[0])*pt[0]
        npt[1]=self.window[2] + (self.window[3]-self.window[2])*pt[1]
        return npt
    def addrandom_neighbor(self,geopt):
        th = np.random.rand()*math.pi*2
        self.current_point = geopt
        localstep = np.random.randint(4,20)
        dx =self.current_point[0] + localstep*np.cos(th)
        dy =self.current_point[1] + localstep*np.sin(th)

        c = sxpColorMan.getrandomcolor('cool',8)
        #    c = color_list[2]
        while dx >self.window[1]:
            dx = dx - np.abs(2*localstep*np.cos(th))
        # dx = self.window[0]
        while dx <self.window[0]:
            dx =dx + np.abs(2*localstep*np.cos(th))
        # dx = self.window[1]
        while dy >self.window[3]:
           dy = dy - np.abs(2*localstep*np.sin(th))
           # dy = self.window[2]
        while dy <self.window[2]:
           dy =dy + np.abs(2*localstep*np.sin(th))
           #dy = self.window[3]

        self.current_point = [dx, dy]
        self.all_point.append(([dx,dy],c))
        return self.current_point
    def add_num_randpoint(self,num):
        for i in range(num):
            self.add_random_point()

    def add_random_point(self):
        th = np.random.rand()*math.pi*2

        dx =self.current_point[0] + self.step*np.cos(th)
        dy =self.current_point[1] + self.step*np.sin(th)

        c = sxpColorMan.getrandomcolor('cool',8)
        #    c = color_list[2]
        while dx >self.window[1]:
            dx = dx - np.abs(2*self.step*np.cos(th))
        # dx = self.window[0]
        while dx <self.window[0]:
            dx =dx + np.abs(2*self.step*np.cos(th))
        # dx = self.window[1]
        while dy >self.window[3]:
           dy = dy - np.abs(2*self.step*np.sin(th))
           # dy = self.window[2]
        while dy <self.window[2]:
           dy =dy + np.abs(2*self.step*np.sin(th))
           #dy = self.window[3]

        self.current_point = [dx, dy]
        self.all_point.append(([dx,dy],c))
        return self.current_point
def main():
    pass;


if __name__ == '__main__':
    main()
