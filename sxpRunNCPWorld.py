# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:
# Purpose: This is to connect pygame to sxpNCPState
# Create Time: 2020/12/18 10:15
# Author: Xiaoping Sun  xiaopingsun@gmail.com//971994252@qq.com
# Copyright:   (c) t 2020
# Licence:     <MIT licence>
# -------------------------------------------------------------------------------

import pygame, math, time, random, os
from pygame.locals import *
from sys import exit

import numpy as np
import sxpColorMan
import sxpNCPState


# 加载资源

def getstartline_xpos(num,wi,ypos):
    interval = wi/(num+1);
    xpos = []
    x = 0
    for i in range(num):
        x = x + (i+1)*interval;
        xpos.append([x,ypos])
    return xpos
def getrandomstart(num,stw,sth,wi,hi):
    r = np.random.rand(num,2)
    r[:,0]=r[:,0]*wi+stw;
    r[:, 1] = r[:, 1] * hi+sth;
    st=[]
    return r.tolist();

WINDOW_W = 1000
WINDOW_H = 600
one_time = 1    # 时间流速（默认1）
scale = 1     # 缩放（默认120）
radius_scale = 1
FPS = 10        # 帧率
point_size = 2  # 点的大小
line_num =100 # the number of lines;
max_line_len =500
b_step = 2
start_xy = (300, WINDOW_H // 2)  # 圆的位置
#start_points=getstartline_xpos(line_num,WINDOW_H,300)
start_points=getrandomstart(line_num,WINDOW_W/3,200,WINDOW_W/4,WINDOW_H/4)
drawtitle = False
drawline = False
drawst = False

line_length =500;
# 波形图参数
b_xy = (600, start_xy[1])  # 波形图原点坐标
b_scale = 1              # 波形图缩放
s_color = (200, 100, 0)    # 波形图颜色
b_color = (100, 200, 0)    # 波形图颜色
l_color = (0,100,200) #line color
b_length = 500             # 波形图显示的长度

#================================#
# 在此处设置函数
# 此处设置的是：f(x) = 1*sin(x) + (1/3)*sin(3x) + (1/5)*sin(5x) + ...
# 这里是一个方形波
# Set the function here
# The settings here are: f(x) = 1*sin(x) + (1/3)*sin(3x) + (1/5)*sin(5x) + ...
# Here's a square wave.
#
# A * sin(v*(θ+ω))
# A->r    v->angle_v    ω->angle
# [r, angle_v, angle]
# fourier_list = [
#     [1    ,  1, 0],
#     [1 / 3,  2, 0],
#     [1 / 5,  3, 0],
#     [1 / 7,  4, 0],
#     [1 / 9,  5, 0],
#     [1 /11, 6, 0],
#     [1 /13, 7, 0],
#     [1 /15, 8, 0],
#     [1 /17, 9, 0],
#     [1 /19, 10, 0]
# ]

# 圆圈的颜色来自于这里，你可以随意添加、删除
color_list = [
    (255, 50, 50),
    (50, 255, 50),
    (50, 50, 255),
    (255, 255, 50),
    (255, 50, 255),
    (50, 255, 255),
    (255, 255, 255)
]

# 初始化pygame
pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 40)
# 创建一个窗口
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("TestWorld")
font = pygame.font.SysFont('microsoftyahei', 16)
# for i in pygame.font.get_fonts():
#     print(i)

world = sxpNCPState.DynWorld()
class Boxin():


    def __init__(self, window,num_pt,start_point,step=3,name='testball'):
        self.window = window
        self.num_pt = num_pt
        self.step = step
        self.start_point = self.mappt(start_point)
        self.current_point =self.start_point
        self.scaley = 1
        self.boxtype ='point'
        self.all_point =[]
        self.name = name
       # self.add_num_point(num_pt)
        self.left = window[0]
        self.top = window[2]
        self.w = window[1]-window[0]
        self.h = window[3]-window[2]
        self.rect = Rect(self.left, self.top, self.w, self.h)
    def mappt(self,pt):
        npt =pt.copy()
        npt[0]=self.window[0]+ (self.window[1]-self.window[0])*pt[0]
        npt[1]=self.window[2]+ (self.window[3]-self.window[2])*pt[1]
        return npt
    def run(self,pause=False):
        #self.add_random_point()
        if pause:
            return
        world.runone()
    def drawworld(self,screen):
        # 画一个圆
        bl = len(world.allperson)
        pygame.draw.rect(screen,color_list[0],self.rect, 3)
        for i in range(bl - 1):
            person = world.allperson[i]
            health_color = person.healthstcolor()
            pt = person.map2windowpos(self.window)
            pygame.draw.circle(screen, health_color, (int(pt[0])
                                                 , int(pt[1]))
                                                 , point_size)

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

    def drawrandom(self, screen):
        # 画一个圆
        bl = len(self.all_point)


        pygame.draw.rect(screen,color_list[0],self.rect, 3)
        for i in range(bl - 1):
            ptc = self.all_point[i]
            b_color = ptc[1][0]
            pt = ptc[0]
            pygame.draw.circle(screen, b_color, (int(pt[0])
                                                 , int(pt[1]))
                                                 , point_size)
    def draw(self,screen,synscale = 1):
        #self.drawrandom(screen)
        self.drawworld(screen)
        return synscale
    def get_radius(self):
        #Assuming these objects are actually spheres, the radius scales with the cube root of
        #the mass.  If you prefer circle, change to the square root.
        return radius_scale*(self.mass**(1.0/3.0))
    @staticmethod
    def get_collided(particle1,particle2):
        r1 = particle1.get_radius()
        r2 = particle2.get_radius()
        both = r1 + r2
        abs_dx = abs(particle2.pos[0] - particle1.pos[0])
        if abs_dx > both: return False
        abs_dy = abs(particle2.pos[1] - particle1.pos[1])
        if abs_dy > both: return False
        #The above lines are just some optimization.  This is the real test.
        if abs_dx*abs_dx + abs_dy*abs_dy > both*both: return False
        return True

    def after_collided(self,particle1,particle2):
        pass
class CurvBox():
    def __init__(self, window,start_point,max_length,linecolor= [255,0,0],name='testy',mass =1):
        self.window = window
        self.originpt = self.mapwindowpt(start_point)
        self.start_point = self.originpt
        self.current_point =self.originpt
        self.scaley = 1
        self.boxtype = 'point'
        self.line_length = max_length
        self.mass = 1;
        self.max_length = max_length
        self.ys = []
        self.name = name
        self.linecolor = linecolor
        self.left = window[0]
        self.top = window[2]
        self.w = window[1]-window[0]
        self.h = window[3]-window[2]
        self.rect = Rect(self.left, self.top, self.w, self.h)
    def run(self):
        self.add_random_point()
    def add_random_point(self):
        pt = (np.random.rand(2,)-0.5)*2

        self.add_point(pt)
    def add_point(self,pt):
        dpt =self.mapcoordwpt(pt)
        self.ys.append(dpt)
        self.current_point = dpt
        if len(self.ys) > self.max_length:
            self.ys.pop(0)
    def mapcoordwpt(self,pt):
        npt =pt.copy()
        npt[0]=self.originpt[0] + (self.window[1]-self.originpt[0])*pt[0]
        npt[1]=self.originpt[1] + (self.window[3]-self.originpt[1])*pt[1]
        return npt
    def mapwindowpt(self,pt):
        npt =pt.copy()
        npt[0]=self.window[0] + (self.window[1]-self.window[0])*pt[0]
        npt[1]=self.window[2] + (self.window[3]-self.window[2])*pt[1]
        return npt
    def draw(self, screen,synscale = 1):
        # 画一个圆
        pygame.draw.rect(screen, color_list[1], self.rect, 3)
        drawline = True
        pygame.draw.circle(screen, self.linecolor, (int(self.current_point[0])
                                             , int(self.current_point[1] * scale))
                                             , point_size)
        bl = len(self.ys)
        if self.scaley > synscale:
            self.scaley = synscale
        else:
            synscale = self.scaley
        if drawline:
            for i in range(bl - 1):
                pygame.draw.line(screen, self.linecolor,
                                 (int(self.ys[i][0] * b_scale), int(self.ys[i][1] * scale)),
                                 (int(self.ys[i+1][0] * b_scale), int(self.ys[i + 1][1] * scale)),
                                 1)

        return synscale
class CurvYBox():
    def __init__(self, window,start_point,max_length,linecolor= [255,0,0],name='testy',mass =1,datakey=['health_ok','cur']):
        self.window = window
        self.boxtype = 'y'
        self.originpt = self.mapwindowpt(start_point)
        self.coordmaxy = self.originpt[1]-self.window[2]
        self.coordminy = self.originpt[1]-self.window[3]
        self.scaley = 1
        self.start_point = self.originpt
        self.current_point =0
        self.line_length = max_length
        self.mass = 1;
        self.max_length = max_length
        self.ys = []
        self.name = name
        self.linecolor = linecolor
        self.left = window[0]
        self.top = window[2]
        self.w = window[1]-window[0]
        self.h = window[3]-window[2]
        self.coordh = np.floor(self.h*2/3)
        self.coordw = np.floor(self.w*2/3)
        self.rect = Rect(self.left, self.top, self.w, self.h)
        self.datakey = datakey
        self.current_value = 0
    def run(self,pause=False):
        #self.add_random_point()
        if pause:
            return
        self.adddata()
        #self.add_random_point()
    def adddata(self):
        y = world.getcurrent(self.datakey[0],self.datakey[1])
        self.add_point(y)
    def add_random_point(self):
        pt = (np.random.rand()-0.5)*2

        self.add_point(pt)
    def add_point(self,y):
        dpt =self.mapcoordywind(y)
        self.ys.append(y)
        self.current_point = y
        if len(self.ys) > self.max_length:
            self.ys.pop(0)
    def mapnormcoordy(self,y):

        ny=self.originpt[1] + (self.window[3]-self.originpt[1])*y
        return ny
    def mapcoordywind(self,y):
        sy = self.scalecoordy(y)
        cy = self.originpt[1] - sy
        return cy
    def mappt(self,y):
        ny = self.originpt[1] - self.scaley*y
        return ny
    def scalecoordy(self,y):
        sy = y
        if y > self.coordmaxy:
            self.scaley = self.coordmaxy/y
            sy = y *self.scaley
        if y < self.coordminy:
            self.scaley = self.coordminy/y
            sy = y*self.scaley
        return sy
    def mapwindowpt(self,pt):
        npt =pt.copy()
        npt[0]=self.window[0] + (self.window[1]-self.window[0])*pt[0]
        npt[1]=self.window[2] + (self.window[3]-self.window[2])*pt[1]
        return npt
    def drawleft2right(self, screen):
        # 画一个圆
        pygame.draw.rect(screen, color_list[1], self.rect, 3)
        drawline = True

        bl = len(self.ys)
        pygame.draw.circle(screen, self.linecolor, (self.originpt[0]
                                             , int(self.current_point * scale))
                                             , point_size)

        if drawline:
            for i in range(bl - 1):
                pygame.draw.line(screen, self.linecolor,
                                 (self.originpt[0] + int((bl - i) * b_scale), int(self.mappt(self.ys[i]) * scale)),
                                 (self.originpt[0] + int((bl - i - 1) * b_scale), int(self.mappt(self.ys[i + 1]) * scale)),
                                 1)
    def draw(self, screen,synscale = 1):
        # 画一个圆
        pygame.draw.rect(screen, color_list[1], self.rect, 3)
        drawline = True

        bl = len(self.ys)
        if self.scaley > synscale:
            self.scaley = synscale
        else:
            synscale = self.scaley
        pygame.draw.circle(screen, self.linecolor, (self.originpt[0]
                                             , int(self.mappt(self.current_point) * scale))
                                             , point_size)

        if drawline:
            for i in range(bl - 1):
                pygame.draw.line(screen, self.linecolor,
                                 (self.originpt[0] + int((i) * b_scale), int(self.mappt(self.ys[i]) * scale)),
                                 (self.originpt[0] + int((i + 1) * b_scale), int(self.mappt(self.ys[i + 1]) * scale)),
                                 1)

        return synscale
class CurvMYBox():
    def __init__(self, window,start_point,max_length,linecolor= [255,0,0],name='testy'):
        self.window = window
        self.boxtype = 'y'
        self.originpt = self.mapwindowpt(start_point)
        self.coordmaxy = self.originpt[1]-self.window[2]
        self.coordminy = self.originpt[1]-self.window[3]
        self.scaley = 1
        self.start_point = self.originpt

        self.line_length = max_length
        self.mass = 1;
        self.max_length = max_length
        self.ys = []
        self.name = name

        self.left = window[0]
        self.top = window[2]
        self.w = window[1]-window[0]
        self.h = window[3]-window[2]
        self.coordh = np.floor(self.h*2/3)
        self.coordw = np.floor(self.w*2/3)
        self.rect = Rect(self.left, self.top, self.w, self.h)
        self.datakey_list = []
        self.current_value = 0
        self.ysdict = {}
        self.datakeydict ={}
        self.current_point = {}
        self.linecolor = {}
    def restart(self):
        for k,v in self.ysdict.items():
            self.ysdict[k]=[]
            self.current_point[k]=0
    def setdata(self,datakey,linecolor):
        datakeyname = datakey[0]+datakey[1]
        self.ysdict[datakeyname]=[]
        self.datakeydict[datakeyname]=datakey
        self.current_point[datakeyname]=0
        self.linecolor[datakeyname]=linecolor
    def run(self,pause=False):
        #self.add_random_point()
        if pause:
            return
        self.adddata()
        #self.add_random_point()
    def adddata(self):
        for datakeyname,datakey in self.datakeydict.items():
            y = world.getcurrent(datakey[0], datakey[1])
            ys = self.ysdict[datakeyname]
            self.scalecoordy(y)#you need to scale large one
            ys.append(y)
            self.current_point[datakeyname] = y
            if len(ys) > self.max_length:
                ys.pop(0)


    def add_random_point(self):
        pt = (np.random.rand()-0.5)*2

        self.add_point(pt)
    def add_point(self,datakeyname,y):
        dpt =self.mapcoordywind(y)
        ys = self.ysdict[datakeyname]
        ys.append(y)
        self.current_point[datakeyname] = y
        if len(ys) > self.max_length:
            ys.pop(0)
    def mapnormcoordy(self,y):

        ny=self.originpt[1] + (self.window[3]-self.originpt[1])*y
        return ny
    def mapcoordywind(self,y):
        sy = self.scalecoordy(y)
        cy = self.originpt[1] - sy
        return cy
    def mappt(self,y):
        ny = self.originpt[1] - self.scaley*y
        return ny
    def scalecoordy(self,y):
        sy = y *self.scaley
        if sy <=self.coordmaxy and sy >= self.coordminy:
            return self.scaley
        sy = y
        if y > self.coordmaxy:
            self.scaley = self.coordmaxy/y
            sy = y *self.scaley
        if y < self.coordminy:
            self.scaley = self.coordminy/y
            sy = y*self.scaley
        return sy
    def mapwindowpt(self,pt):
        npt =pt.copy()
        npt[0]=self.window[0] + (self.window[1]-self.window[0])*pt[0]
        npt[1]=self.window[2] + (self.window[3]-self.window[2])*pt[1]
        return npt
    def drawleft2right(self, screen,datakeyname):
        # 画一个圆
        pygame.draw.rect(screen, color_list[1], self.rect, 3)
        drawline = True

        bl = len(self.ys)
        pygame.draw.circle(screen, self.linecolor, (self.originpt[0]
                                             , int(self.current_point * scale))
                                             , point_size)
        ys = self.ysdict[datakeyname]
        if drawline:
            for i in range(bl - 1):
                pygame.draw.line(screen, self.linecolor,
                                 (self.originpt[0] + int((bl - i) * b_scale), int(self.mappt(ys[i]) * scale)),
                                 (self.originpt[0] + int((bl - i - 1) * b_scale), int(self.mappt(ys[i + 1]) * scale)),
                                 1)
    def draw(self, screen,synscale = 1):
        # 画一个圆
        pygame.draw.rect(screen, color_list[1], self.rect, 3)
        drawline = True


        if self.scaley > synscale:
            self.scaley = synscale
        else:
            synscale = self.scaley

        for datakeyname,ys in self.ysdict.items():
            current_point = self.current_point[datakeyname]
            linecolor = self.linecolor[datakeyname]
            pygame.draw.circle(screen, linecolor, (self.originpt[0]
                                                        , int(self.mappt(current_point) * scale))
                               , point_size)
            bl = len(ys)
            if drawline:
                for i in range(bl - 1):
                    pygame.draw.line(screen, linecolor,
                                     (self.originpt[0] + int((i) * b_scale), int(self.mappt(ys[i]) * scale)),
                                     (self.originpt[0] + int((i + 1) * b_scale), int(self.mappt(ys[i + 1]) * scale)),
                                     1)

        return synscale
    def drawlegend(self,screen,x,y):
        i = 0
        for datakeyname,datakey in self.datakeydict.items():
            if self.boxtype == 'y':
                linecolor = self.linecolor[datakeyname]
                current_point = self.current_point[datakeyname]
                v = '{}：{:.2f}'.format(datakey[0], current_point)
                text_obj = font.render(v, 1, (255, 255, 255))
                screen.blit(text_obj, (x + i * 200, y))
                pygame.draw.circle(screen, linecolor, (int(x + i * 200)
                                                           , int((y + 20)) * scale)
                                   , point_size)
                i = i + 1


rline_list = []
box_window = [10,400,100,500]
box1 = Boxin(box_window,100,[0,0.50],step=5)
rline_list.append(box1)

curv_window = [10+500,400+500,100,500]
maxlen = curv_window[1]-curv_window[0]
#curv1 = CurvYBox(curv_window,[0,0.5],maxlen,linecolor= color_list[1],name='health_wuzheng', datakey=['health_wuzheng','cur'])
#rline_list.append(curv1)

#curv2 = CurvYBox(curv_window,[0,0.5],maxlen,linecolor= color_list[3],name='health_recover', datakey=['health_recover','cur'])
#rline_list.append(curv2)

#curv3 = CurvYBox(curv_window,[0,0.5],maxlen,linecolor= color_list[0],name='health_sick', datakey=['health_sick','cur'])
#rline_list.append(curv3)

curv = CurvMYBox(curv_window,[0,0.5],maxlen,linecolor= color_list[0],
                 name='sim')

curv.setdata(['health_wuzheng','cur'],color_list[1])
#curv.setdata(['health_recover','cur'],color_list[3])
curv.setdata(['health_sick','cur'],color_list[0])
rline_list.append(curv)

clock = pygame.time.Clock()

pause = True
# 游戏主循环
restart = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            elif event.key == K_SPACE:
                pause = not pause
            elif event.key == K_r:
                restart = True
            elif event.key == K_LEFT and one_time>0.1:
                one_time *= 0.9
                one_time = max(one_time,0.1)
            elif event.key == K_RIGHT and one_time<10:
                one_time *= 1.1
            elif (event.key == K_EQUALS or event.key == K_PLUS) and scale<800:
                #scale *= 1.1
                b_step = b_step + 1

            elif event.key == K_MINUS and scale>0.001:
                #scale *= 0.9
                #scale = max(scale,0.001)
                b_step = b_step - 1
                b_step = max(b_step, 0)
            elif event.key == K_l and b_scale<10:
                b_scale *= 1.1
            elif event.key == K_k and b_scale>0.1:
                b_scale *= 0.9
                b_scale = max(b_scale,0.1)
            else:
                print(type(event.key),event.key)

    # 将背景图画上去
    screen.fill((0, 0, 0))
    # 运行
    #draw the moving points
    if restart:
        world.restart()
        curv.restart()
        restart = False
    synscale = 1
    for i, rline in  enumerate(rline_list):

        rline.run(pause)
        synscale = rline.draw(screen,synscale)

    # 画波形



    # 画文字
    text_obj = font.render('Dynmic Sim of Spreading of Virus', 1, (255,255,255))
    screen.blit(text_obj, (10, 10))
    text_obj = font.render('key space :start/resume/pause;'.format(b_step), 1, (255,255,255))
    screen.blit(text_obj, (10, 30))
    text_obj = font.render('key r :restart'.format(b_step), 1, (255, 255, 255))
    screen.blit(text_obj, (350, 30))
    text_obj = font.render('FPS：{:.1f}'.format(clock.get_fps()), 1, (255,255,255))
    screen.blit(text_obj, (10,55))
    curv.drawlegend(screen,150,55)
    i = 0
    # for box in rline_list:
    #     if box.boxtype =='y':
    #         v = '{}：{:.2f}'.format(box.name,box.current_point)
    #         text_obj = font.render(v, 1, (255, 255, 255))
    #         screen.blit(text_obj, (150+i*200, 55))
    #         pygame.draw.circle(screen, box.linecolor, (int(150+i*200)
    #                                                     , int((55+20)) * scale)
    #                            , point_size)
    #         i = i + 1

    pygame.display.update()
    time_passed = clock.tick(FPS)


def main():
    pass


if __name__ == '__main__':
    main()
def main():
    pass;


if __name__ == '__main__':
    main()
