#coding=utf-8
#-------------------------------------------------------------------------------
# Name:        ****
# Purpose:
#
# Author:      Sun Xiaoping
#
# Created:     03/10/2020
# Copyright:   (c) sunxp 971994252@qq.com 2020
# Licence:     <mit licence>
#-------------------------------------------------------------------------------

#---------------In this model-------------
print('''
#---------------in this model------------
we will simulate how a Covid is spreading and then fading to end
not because the infected number of people is dropping 
but because the isolating stregy works as more and more people are infected
The core in this model is infectothers() which is called when geofree() is called.
That is, we only consider those who are still in free geo state and simulate their
infection chains.
In this model, we update pub_risk and home_risk according to the number of infecious
But this immediately feedback will make the infection number
continue to fluctuate as time goes by. 
It is mainly because the feed back is so immediatly, people wont' wait for any longer time
for isolation, so you need to add an isolation delay period for feed back.
#----------------------------------------
''')

#this file contains some classes that are to read text files

import sxpColorMan
import numpy as np
import sxpGeoMap
#-----init---state
thisfilename = __file__
sxpColorMan.parsestatefromfile(thisfilename)
sxpColorMan.parsestatefromfile(thisfilename)

global_cum_st = sxpColorMan.getstatdict()
global_current_st =sxpColorMan.getstatdict()

global_current_list = []
global_cum_list = []
global_geomap = sxpGeoMap.GeoMap(window=[0,400,0,400],originpt=[0.5,0.5],step=8)
print_update = False
record_list = False

class InfectPersion:
    def __init__(self,id,t=0):

        self.hv = 'health_init'
        self.gv = 'geo_init'
        self.mv = 'med_init'
        global_current_st[self.hv] = 1
        global_current_st[self.gv] = 1
        self.nhv = self.hv
        self.ngv = self.gv
        self.nmv = self.mv
        self.gv_days = 0
        self.hv_days = 0
        self.mv_days = 0
        self.geli_days = 14
        self.gv_state_list=[]
        self.hv_state_list = []
        self.mv_state_list = []

        self.homenumber = np.random.randint(1,4)
        self.familynumber = np.random.randint(1,4)
        self.colleaguenumber = np.random.randint(4,10)
        self.pubeverday=np.random.randint(10)
        self.maxinfecteveryday = np.random.randint(10)
        self.infect_new = 0
        self.infect_new_list = []
        self.nextinfecttype = "pub"
        self.nextinfectlevel = 2
        self.myinfectlevel = 1
        self.myinfecttype = 'pub'
        self.allinfect=0
        self.population = np.power(10,4)
        self.rect_w= 400;
        self.rect_h = 400;
        self.id = id
        self.xy = global_geomap.add_random_point()

        self.c = 0
        self.t = 0
        self.startinfect = -1
        self.endinfect = -1
        self.riskmem = []
        self.riskmemsize= 10
    def initinfect(self,hv='health_wuzheng',gv='geo_free'):
        self.nhv = hv
        self.ngv = gv
        self.geoupdate()
        #global_current_st[self.ngv] += 1
        #global_current_st[self.nhv] += 1
    def healthcolor(self):
        return sxpColorMan.healthstcolor(self.hv)
    def map2windowpos(self,window):
        return global_geomap.map2window2pt(self.xy, window)
    def getrandom_neighborpos(self):
        return global_geomap.addrandom_neighbor(self.xy)
    def healthstcolor(self):
        return sxpColorMan.healthstcolor(self.hv)
    def geostcolor(self):
        return sxpColorMan.geostcolor(self.gv)

    def draw(self):
        pass
    def record(self,current_st):
        self.t = self.t + 1
        if self.hv =='health_wuzheng' and self.startinfect == -1:
            self.startinfect = self.t
        if self.hv in ['health_recover'] and self.endinfect == -1:
            self.endinfect = self.t
        updated = False
        lasthv = [self.hv, self.hv_days]
        if self.nhv == self.hv:
            self.hv_days += 1
        else:
            if print_update:
                print('^^^update^',self.hv,self.nhv)
                print(current_st[self.hv],current_st[self.nhv])
            current_st[self.hv] -= 1
            current_st[self.nhv] += 1
            if print_update:
                print(current_st[self.hv], current_st[self.nhv])
                print('^^^^^^^')
            self.hv_days = 1
            self.hv = self.nhv
            global_cum_st[self.nhv] += 1
            updated = True

        lastgv = [self.gv, self.gv_days]
        if self.ngv == self.gv:
            self.gv_days +=1
        else:
            if print_update:
                print('-update-',self.gv,self.ngv)
                print(current_st[self.gv],current_st[self.ngv])
            current_st[self.gv] -= 1
            current_st[self.ngv] += 1
            if print_update:
                print(current_st[self.gv], current_st[self.ngv])
                print('--------')
            self.gv_days = 1
            self.gv = self.ngv
            global_cum_st[self.ngv] += 1
            updated = True


        if updated and record_list:
            self.hv_state_list.append([lasthv,self.nhv])
            self.gv_state_list.append([lastgv,self.ngv])

        # if self.nmv == self.mv:
        #     self.mv_days +=1
        # else:
        #     self.mv_state_list.append([self.mv,self.mv_days])
        #     self.mv_days = 0
    def geoend(self):
      #  self.record(global_current_st)
        self.ngv = 'geo_end'
        self.nhv = 'health_end'
        #self.record(global_current_st)
        global_current_st[self.ngv] += 1
        global_current_st[self.nhv] += 1
        if record_list:
            self.hv_state_list.append([self.hv, self.nhv])
            self.gv_state_list.append([self.gv, self.ngv])
    def geoupdate(self):

        self.record(global_current_st)

        if self.gv == 'geo_free':
            self.geo_movefree()
            self.infectother()
        if self.gv == 'geo_kanbing':
            self.geo_kanbing()
        if self.gv == 'geo_home_geli':
            self.geo_home_geli()
        if self.gv == 'geo_zhiliao_zhuyuan':
            self.zhiliao_zhuyuan()
        if self.gv == 'geo_zhiliao_icu':
            self.zhiliao_icu()
        if self.gv == 'geo_zhiliao_geli':
            self.zhiliao_geli()
        if self.gv == 'geo_si':
                self.si()
        if self.gv == 'geo_icu_si':
                self.si()
    def behighrisk(self):
        self.highrisk = self.allinfect/self.population
        return self.highrisk
    def behighrisk_ganran(self):
        return 0.2

    def infectother(self):
    #    self.infect_new_list = []
        if self.hv == 'health_ok':
            self.infect_new = 0
            return
    #        self.infect_new_list.append(0)
        if self.hv == 'health_recover':
            self.infect_new = 0
            return
        pstayhome = global_current_st['health_risk']
        region = self.probsel({'pub':1-pstayhome,'home':pstayhome})
        self.nextinfecttype = region
        self.nextinfectlevel = self.myinfectlevel + 1
        #ppubinfect = 1- global_current_st['health_risk']
        ppubinfect = global_current_st['health_pubinfectrisk']
        homeextend = 2
        if self.hv == 'health_wuzheng':
            if region == 'pub':
                new_num = self.probnum(0, 50, ppubinfect)
            if region == 'home':
                phomeextend = 1./np.power(3,self.nextinfectlevel)
                if self.homenumber <=0:
                    new_num = 0
                else:
                    new_num = self.probnum(0, self.homenumber, phomeextend)
                self.homenumber = self.homenumber-new_num
                if self.homenumber <0:
                    self.homenumber = 0
                self.myinfecttype = 'home'
            if new_num >= self.maxinfecteveryday:
                new_num = self.maxinfecteveryday
            self.infect_new = new_num
     #       self.infect_new_list.append(new_num)
        if self.hv == 'health_light':
            if region == 'pub':
                new_num = self.probnum(0, 10, ppubinfect)
            if region == 'home':
                phomeextend = 1./np.power(3, self.nextinfectlevel)
                if self.homenumber <=0:
                    new_num = 0
                else:
                    new_num = self.probnum(0, self.homenumber, phomeextend)
                self.homenumber = self.homenumber-new_num
                if self.homenumber <0:
                    self.homenumber = 0
                self.myinfecttype = 'home'

            if new_num >= self.maxinfecteveryday:
                new_num = self.maxinfecteveryday
            self.infect_new = new_num
     #       self.infect_new_list.append(new_num)
        if self.hv == 'health_mid':
            if region == 'pub':
                new_num = self.probnum(1, 2, ppubinfect/10)

            if region == 'home':
                homeextend = np.power(3,self.nextinfectlevel)
                phomeextend = 1./np.power(3, self.nextinfectlevel)
                if self.homenumber <=0:
                    new_num = 0
                else:
                    new_num = self.probnum(0, self.homenumber, phomeextend)
                self.homenumber = self.homenumber-new_num
                if self.homenumber <0:
                    self.homenumber = 0
                self.myinfecttype = 'home'

            if new_num >= self.maxinfecteveryday:
                new_num = self.maxinfecteveryday
            self.infect_new = new_num
    #        self.infect_new_list.append(new_num)
        if self.hv == 'health_zhong':
            if region == 'pub':
                new_num = self.probnum(1, 0, ppubinfect/10)
            if region == 'home':
                phomeextend = 1./np.power(4, self.nextinfectlevel)
                if self.homenumber <=0:
                    new_num = 0
                else:
                    new_num = self.probnum(0, self.homenumber, phomeextend)
                self.homenumber = self.homenumber-new_num
                if self.homenumber <0:
                    self.homenumber = 0
                self.myinfecttype = 'home'


            if new_num >= self.maxinfecteveryday:
                new_num = self.maxinfecteveryday

            self.infect_new = new_num
    #        self.infect_new_list.append(new_num)
        if self.hv == 'health_huifu':
            self.infect_new = 0
    #        self.infect_new_list.append(0)

        if self.infect_new >0 and region == 'home':
            print('infect:',self.hv, region,self.infect_new,self.homenumber,homeextend)
    def geo_movefree(self):
        self.nmv = 'med_no'
        if self.hv == 'health_ok':
            highrisk = self.behighrisk()
            self.ngv = 'geo_free'
            self.nhv = self.probsel({'health_highrisk':highrisk,'health_ok':1-highrisk})
        if self.hv == 'health_recover':
            highrisk = 0
            self.ngv = 'geo_free'
            self.nhv = self.probsel({'health_highrisk': highrisk,'health_recover':1-highrisk})
        if self.hv == 'health_highrisk':
            pganran = self.behighrisk_ganran()
            self.nhv = self.probsel({'health_ok':1-pganran,'health_wuzheng':pganran})
            if self.nhv != 'health_ok':
                self.ngv = self.probsel({'geo_free':0.99, 'geo_zhiliao_geli':0,'geo_home_geli':0.01})
            else:
                self.ngv = 'geo_free'
        if self.hv == 'health_wuzheng':
            self.nhv = self.probsel({'health_huifu':0.001, 'health_light':0.1, 'health_wuzheng':0.9})
            self.ngv = self.probsel({'geo_free':0.99,'geo_home_geli':0.01,'geo_zhiliao_geli':0})
        if self.hv == 'health_light':
            self.nhv = self.probsel({'health_huifu': 0.005, 'health_light': 0.3, 'health_mid': 0.1})
            if self.nhv != 'health_huifu':
                self.ngv = self.probsel({'geo_free': 0.88, 'geo_kanbing': 0.12,'geo_home_geli':0.12,'geo_zhiliao_geli':0})
            else:
                self.ngv = 'geo_free'
        if self.hv == 'health_mid':

            self.nhv = self.probsel({'health_huifu': 0.1, 'health_mid':0.3, 'health_zhong':0.3})
            if self.nhv != 'health_huifu':
                self.ngv = self.probsel({'geo_kanbing': 0.8, 'geo_home_geli':0.2})
            else:
                self.ngv = 'geo_free'

        if self.hv == 'health_zhong':
            self.nhv = self.probsel({'health_huifu': 0.1, 'health_zhong':0.4, 'health_si':0.1})
            if self.nhv != 'health_huifu':
                self.ngv = self.probsel({'geo_kanbing': 0.95, 'geo_home_geli': 0.05})
            else:
                self.ngv = 'geo_home_geli'

        if self.hv == 'health_huifu':
            self.nhv = self.probsel({'health_huifu': 0.8, 'health_recover':0.2})
            if self.nhv == 'health_recover':
                self.ngv = 'geo_free'
            else:
                self.ngv = 'geo_home_geli'

        if self.hv == 'health_si':
            self.nhv = 'health_si'
            self.ngv = 'geo_si'

    def geo_home_geli(self):
        self.nmv = 'med_no'
        if self.hv == 'health_ok':
            self.ngv = 'geo_free'
            self.nhv = self.probsel({'health_highrisk':0,'health_ok':1})

        if self.hv == 'health_huifu':
            self.nhv = self.probsel({'health_huifu':0.7, 'health_recover':0.3})
            self.ngv = 'geo_home_geli'

        if self.hv == 'health_recover':
            self.ngv = 'geo_free'
            self.nhv = 'health_recover'

        if self.hv == 'health_highrisk':
            self.nhv = self.probsel({'health_ok':0.98,'health_wuzheng':0.02})
            self.ngv = self.probsel({'geo_kanbing':0,'geo_home_geli':1,'geo_zhiliao_geli':0})

        if self.hv == 'health_wuzheng':

            self.nhv = self.probsel({'health_huifu':0.08, 'health_light':0.5, 'health_wuzheng':0.5})
            self.ngv = self.probsel({'geo_kanbing':0.08,'geo_home_geli':0.90,'geo_zhiliao_geli':0})

        if self.hv == 'health_light':
            self.nhv = self.probsel({'health_huifu':0.10,'health_light':0.13, 'health_mid':0.20})
            self.ngv = self.probsel({'geo_kanbing':0.2,'geo_home_geli':0.8,'geo_zhiliao_geli':0})

        if self.hv == 'health_mid':
            self.nhv = self.probsel({'health_huifu':0.2, 'health_mid':0.4, 'health_zhong':0.4})
            self.ngv = self.probsel({'geo_kanbing':0.8,'geo_home_geli':0.2})
        if self.hv == 'health_zhong':

            self.nhv = self.probsel({'health_huifu':0.3, 'health_zhong':0.5, 'health_si':0.2})
            self.ngv = self.probsel({'geo_kanbing':1,'geo_home_geli':0})
        if self.hv == 'health_si':
            self.nhv = 'health_si'
            self.ngv = 'geo_si'
    def geo_kanbing(self):
        if self.hv in ['health_ok']:
            self.nhv = 'health_ok'
            self.ngv = 'geo_free'
        if self.hv == 'health_huifu':
            self.nhv = 'health_huifu'
            self.ngv = 'geo_home_geli'
        if self.hv == 'health_recover':
            self.nhv = 'health_recover'
            self.ngv = 'geo_home_geli'
        if self.hv in ['health_wuzheng']:
            self.nmv=self.probsel({'med_no':0.01,'med_quezhen':0.99})
            if self.nmv == 'med_no':
                self.ngv = 'geo_home_geli'
            if self.nmv == 'med_quezhen':
                self.ngv = 'geo_zhiliao_geli'

        if self.hv == 'health_light':
            med_dec=self.probsel({'med_no':0.005,'med_quezhen':0.999})
            if med_dec == 'med_no':
                ngv = 'geo_home_geli'
            if med_dec == 'med_quezhen':
                ngv = 'geo_zhiliao_zhuyuan'
            self.nmv = med_dec
            self.ngv = ngv
        if self.hv == 'health_mid':
            med_dec=self.probsel({'med_no':0.0001,'med_quezhen':0.9999})
            if med_dec == 'med_no':
                ngv = 'geo_home_geli'
            if med_dec == 'med_quezhen':
                ngv = 'geo_zhiliao_zhuyuan'
            self.nmv = med_dec
            self.ngv = ngv
        if self.hv == 'health_zhong':
            med_dec=self.probsel({'med_no':0.0,'med_quezhen':1})
            if med_dec == 'med_no':
                ngv = 'geo_home_geli'
            if med_dec == 'med_quezhen':
                zhiliao = self.probsel({'geo_zhiliao_zhuyuan':0.9,'geo_zhiliao_icu':0.1})
                if zhiliao == 'geo_zhiliao_zhuyuan':
                    ngv = 'geo_zhiliao_zhuyuan'
                if zhiliao == 'geo_zhiliao_icu':
                    ngv = 'geo_zhiliao_icu'
            self.nmv = med_dec
            self.ngv = ngv
        self.nhv = self.hv
    def zhiliao_geli(self):
        if self.hv == 'health_ok':
            if self.hv_days>=self.geli_days:
                self.nhv = 'health_ok'
                self.ngv = 'geo_free'
            else:
                self.ngv = "geo_zhiliao_geli"
                self.nhv = 'health_ok'
        if self.hv == 'health_recover':
         #   self.ngv = 'geo_zhiliao_geli'
            self.nhv = 'health_recover'
        if self.hv_days >= self.geli_days:
            self.ngv = 'geo_free'
        else:
            self.ngv = 'geo_zhiliao_geli'
        if self.hv == 'health_highrisk':
            self.nhv=self.probsel({'health_wuzheng':0.05,'health_light':0.02,'health_ok':0.9})
        if self.hv == 'health_wuzheng':
            nhv = self.probsel({'health_light':0.4, 'health_wuzheng':0.3, 'health_huifu':0.01})
            self.nhv = nhv
        if self.hv == 'health_light':
            self.nhv = self.probsel({'health_light':0.4, 'health_mid':0.2, 'health_huifu':0.01})
            self.ngv = "geo_zhiliao_zhuyuan"
        if self.hv == 'health_mid':
            self.nhv = self.probsel({'health_mid':0.4, 'health_zhong':0.4, 'health_huifu':0.01})
            self.ngv = "geo_zhiliao_zhuyuan"
        if self.hv == 'health_zhong':
            self.nhv = self.probsel({ 'health_zhong':0.4,'health_icu_zhong':0.2,  'health_huifu':0.01})
            self.ngv = 'geo_zhiliao_zhuyuan'
        if self.hv == 'health_huifu':
            self.nhv = self.probsel({'health_huifu':0.4, 'health_recover':0.2})
            self.ngv = 'geo_zhiliao_geli'
        if self.hv == 'health_icu_zhong':
            self.ngv = self.probsel({'geo_zhiliao_icu':0.4, 'geo_zhiliao_zhuyuan':0.8})
            self.nhv = self.probsel({'health_icu_zhong':0.9, 'health_huifu':0.01})
    def zhiliao_zhuyuan(self):
        if self.hv == 'health_wuzheng':
            self.nhv= self.probsel({'health_light':0.4,'health_wuzheng':0.4,'health_huifu':0.4})
            self.ngv = "geo_zhiliao_zhuyuan"
        if self.hv == 'health_light':
            self.nhv= self.probsel({'health_light':0.4,'health_mid':0.2,'health_huifu':0.2})
            self.ngv = "geo_zhiliao_zhuyuan"
        if self.hv == 'health_mid':
            self.nhv = self.probsel({'health_mid':0.4,'health_zhong':0.2,'health_huifu':0.2})
            self.ngv = "geo_zhiliao_zhuyuan"
        if self.hv == 'health_zhong':
            self.nhv = self.probsel({'health_zhong':0.4,'health_icu_zhong':0.2,'health_si':0.05,'health_huifu':0.2})
            self.ngv = "geo_zhiliao_zhuyuan"
        if self.hv == 'health_huifu':
            self.nhv = self.probsel({'health_huifu':0.4,'health_recover':0.2})
            self.ngv = "geo_zhiliao_zhuyuan"
        if self.hv == 'health_recover':
            self.nhv='health_recover'
            self.ngv = 'geo_free'
        if self.hv == 'health_si':
            self.nhv = 'health_si'
            self.ngv = 'geo_si'
        if self.hv == 'health_icu_zhong':
            ngv = self.probsel({'got_icu':0.8,'no_icu':0.2})
            if ngv == 'got_icu':
                self.ngv = 'geo_zhiliao_icu'
            else:
                self.ngv = 'geo_zhiliao_zhuyuan'
            self.nhv = self.probsel({'health_icu_zhong':0.4, 'health_si':0.05, 'health_huifu':0.1})
    def zhiliao_icu(self):
        if self.hv == 'health_zhong':
            self.nhv = self.probsel({'health_zhong':0.2,'health_icu_zhong':0.2,'health_si':0.05,'health_huifu':0.2})
            self.ngv = "geo_zhiliao_icu"

        if self.hv == 'health_icu_zhong':
           self.nhv = self.probsel({'health_icu_zhong':0.4, 'health_si':0.1, 'health_huifu':0.3})
           self.ngv = 'geo_zhiliao_icu'
        if self.hv == 'health_huifu':
            self.nhv = self.probsel({'health_huifu':0.4,'health_recover':0.2})
            self.ngv = 'geo_zhiliao_zhuyuan'
        if self.hv == 'health_recover':
            self.nhv='health_recover'
            self.ngv = 'geo_free'
        if self.hv == 'health_si':
            self.nhv = 'health_si'
            self.ngv = 'geo_icu_si'
    def si(self):
        self.nhv = 'health_si'
        self.ngv = 'geo_si'
    def probnum(self,m,n,p):
        if m>n:
            return 0
        if m==n:
            r = np.random.rand()
            if r<p:
                return 1
            else:
                return 0
        else:
            r = np.random.randint(m,n)
        s =0
        for i in range(r):
            if np.random.rand()<=p:
                s = s +1
        return s
    def probsel(self,probdist):
        r = np.random.random()
        sp = []
        i =0
        si ={}
        t = 0
        for s,p in probdist.items():
            sp.append(p)
            t = t + p
            si[i]=s
            i = i + 1

        sp = np.array(sp) /t
        sp = sp.reshape(1,i).tolist()
        #print(sp.shape,np.sum(sp),i,1,sp)
        #ns = np.random.choice(i,1,sp)
        ns = chooseone(i,sp)
        return si[ns]
    def showstatelist(self):
        print('----health geo state----',self.id)
        for i,s in enumerate(self.hv_state_list):
            print('state:',i,'health:',s,'geo:',self.gv_state_list[i])

class DynWorld():
    def __init__(self,max_n=10000):
        self.autorestart = False
        self.need_restart = False
        self.allperson = []
        p = InfectPersion(id = 0)
        #p.initinfect('health_mid','geo_free')
        p.initinfect('health_wuzheng', 'geo_free')

        self.id = 0
        self.t = 0
        self.allperson.append(p)
    def restart(self):

        self.need_restart=False
        resetst(global_current_st)
        resetst(global_cum_st)
        global_cum_list = []
        global_current_list = []
        self.allperson = []
        del self.allperson
        self.allperson = []
        self.t = 0
        self.id = 0
        p = InfectPersion(id = 0)
        #p.initinfect('health_mid','geo_free')
        p.initinfect('health_wuzheng', 'geo_free')
        self.allperson.append(p)


    def showstatelist(self,idx):
        p = self.allperson[idx]
        p.showstatelist()
    def endall(self):
        for each in self.allperson:
            each.geoend()
    def runone(self):
        self.t += 1

        newone =[]

        for each in self.allperson:
            each.geoupdate()
            if each.infect_new==0:
                continue
            new_infect = each.infect_new
            for i in range(new_infect):
                self.id += 1
                p = InfectPersion(id = self.id)
                p.myinfecttype = each.nextinfecttype
                p.myinfectlevel = each.nextinfectlevel
                p.initinfect('health_highrisk','geo_free')
                p.xy = each.getrandom_neighborpos()
                newone.append(p)

        for each in newone:
            self.allperson.append(each)

        print('----person num:',len(self.allperson))
        self.num_infect = len(self.allperson)
        global_current_st['health_newinfect'] = len(newone)
        self.collecglobalinfo()
        self.showcur(printst='detail')
        if self.autorestart:
            if global_current_st['health_sick']==0:
                print('---restart automatically, after 0 sick')
                self.need_restart= True
    def draw(self,window,pygame,screen,point_size = 2,scale=1):
        self.runone()
        for each in self.allperson:
            each.geoupdate()
            pt = each.getpos(window)
            stcolor = each.healthstcolor()
            pygame.draw.circle(screen, stcolor, (int(pt[0]* scale)
                                             , int(pt[1]* scale))
                               , point_size)
    def collecglobalinfo(self):
        global_current_st['health_allcontect'] = len(self.allperson)
        nbing = global_current_st['health_wuzheng']+global_current_st['health_light'] + \
        global_current_st['health_mid'] + \
        global_current_st['health_zhong'] + \
        global_current_st['health_icu_zhong']
        global_current_st['health_sick'] = nbing
        global_current_st['health_risk'] = min(nbing*1.0/100,1.0)
        global_current_st['health_pubinfectrisk'] = 1- global_current_st['health_risk']
    def showcur(self,printst='breif'):

        if printst=='breif':
            print('ok',global_current_st['health_ok'],
                  'sick',global_current_st['health_sick'],
                  'dead',global_current_st['health_si'],
                  'recover',global_current_st['health_recover'])
        if printst=='detail':
            print('ok',global_current_st['health_ok'],
                  'health_risk',global_current_st['health_risk'],
                  'pub_risk', global_current_st['health_pubinfectrisk'],
                  'newone', global_current_st['health_newinfect'],
                  'wuzheng',global_current_st['health_wuzheng'],
                  'light', global_current_st['health_light'],
                  'mid', global_current_st['health_mid'],
                  'zhong', global_current_st['health_zhong'],
                  'icu', global_current_st['health_icu_zhong'],
                  'dead',global_current_st['health_si'],
                  'recover',global_current_st['health_recover'])
            print('geo_free',global_current_st['geo_free'],
                  'geo_kanbing',global_current_st['geo_kanbing'],
                  'geo_home_geli', global_current_st['geo_home_geli'],
                  'geo_zhiliao_zhuyuan', global_current_st['geo_zhiliao_zhuyuan'],
                  'geo_zhiliao_icu', global_current_st['geo_zhiliao_icu'],
                  'geo_zhiliao_geli', global_current_st['geo_zhiliao_geli'],
                  'geo_si',global_current_st['geo_si'],
                  'geo_icu_si',global_current_st['geo_icu_si'])
    def getcurrent(self,datakey,md='cur'):

        if md=='cur':
          #  print(global_current_st[datakey])
            return global_current_st[datakey]
        if md == 'cum':
         #   print(global_cum_st[datakey])
            return global_cum_st[datakey]
def record_st(st_dict,global_list):
    global_list.append(st_dict.copy())
def resetst(st_dict):
    for k,v in st_dict.items():
        st_dict[k]=0
def showcurrent(keys=[]):
    print('----current_key-st---')
    for k,v in global_current_st.items():
        if k in keys:
            print(k,v)
def showglobalcumnonzeor():
    print('----global cum nonzero-st---')
    for k,v in global_cum_st.items():
        if v>0:
            print(k,v)

def showcurrentnonzero():
    print('----current_nozero-st---')
    for k,v in global_current_st.items():
        if v>0:
            print(k,v)
def chooseone(num_state,probdist):
    r = np.random.rand()
    pdf = np.cumsum(probdist)
    for i,p in enumerate(pdf):
        if r < p:
            break
    return i
def testprob():
    p = InfectPersion(0,'health_ok')
    highrisk = 0.5
    for i in range(100):
        print(p.probsel({'health_huifu': 0.3, 'health_recover': 0.3,'health_zhong':0.3}))
def test():
    resetst(global_current_st)
    world = DynWorld()
    for i in range(10000):
        world.runone()
        record_st(global_current_st,global_current_list)
        record_st(global_cum_st, global_cum_list)
        print('*******',i,'people num:',world.num_infect)
        showcurrent('geo_free')
        showcurrentnonzero()
    world.endall()
    world.showstatelist(0)
    showglobalcumnonzeor()
allstate = '''
geo_init
geo_free
geo_end
geo_kanbing
geo_home_geli
geo_zhiliao_zhuyuan
geo_zhiliao_icu
geo_zhiliao_geli
geo_si
geo_icu_si
health_init
health_wuzheng
health_recover
health_end
health_ok
health_light
health_mid
health_zhong
health_huifu
health_highrisk
health_si
health_icu_zhong
'''
def getstatistic():
    current_data ={}
    current_data['geo_init'] = global_current_st['geo_init']
    current_data['health_ok'] = global_current_st['health_ok']
    current_data['health_highrisk'] = global_current_st['health_highrisk']
    current_data['health_wuzheng'] = global_current_st['health_wuzheng']
    current_data['health_light'] = global_current_st['health_light']
    current_data['health_zhong'] = global_current_st['health_zhong']
    current_data['health_icu_zhong'] = global_current_st['health_icu_zhong']
    current_data['health_recover'] = global_current_st['health_recover']

    cum_data ={}
    cum_data['geo_init'] = global_cum_st['geo_init']
    cum_data['health_ok'] = global_cum_st['health_ok']
    cum_data['health_highrisk'] = global_cum_st['health_highrisk']
    cum_data['health_wuzheng'] = global_cum_st['health_wuzheng']
    cum_data['health_light'] = global_cum_st['health_light']
    cum_data['health_zhong'] = global_cum_st['health_zhong']
    cum_data['health_icu_zhong'] = global_cum_st['health_icu_zhong']
    cum_data['health_recover'] = global_cum_st['health_recover']

    data ={}
    data['current']=current_data
    data['cum']=cum_data

    return data
def main():
    print('---------start run main--------')
    #testprob()
    test()


if __name__ == '__main__':
    main()
