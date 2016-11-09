#/usr/bin/python
import math
import numpy as np
import pylab as pl
import random
import csv 
import os
from operator import add 

timeline=24*60*60*7
ss=[0.0]*timeline
s1=[0.0]*timeline
s2=[0.0]*timeline
s3=[0.0]*timeline
s4=[0.0]*timeline
s5=[0.0]*timeline
s6=[0.0]*timeline
s7=[0.0]*timeline
s8=[0.0]*timeline

def on_off(p_ON_t,p_OFF_t,lamada_,s_t,e_t):
  p_ON,p_OFF=p_ON_t,p_OFF_t
  s,e=s_t,e_t
  NN=e-s+1
  p=[0.0]*timeline
  for i in range(s,e):
    p[i]=p_OFF
  to_stop = int(NN*(1-lamada_))
  for i in range(s,to_stop):
    p[i]=p_ON
  return p


def decay(p_peak_,p_active_,lamada_,s_t,e_t):
  "Basic Decay Model"
  s,e=s_t,e_t
  p_active,p_peak,lamada=p_active_,p_peak_,lamada_
  NN=e-s+1
  p=[0.0]*timeline
  N=[0]*timeline
  for j in range(1,timeline+1):
    N[j-1]=j
  for i in range(1,NN+1):
    if s+i-1 <= timeline:
      p[s+i-1]=p_active+(p_peak-p_active)*math.exp(-lamada*i)
  #print s+i-1
  #pl.xlim(1,timeline)
  #pl.ylim(1400,1470)
  #pl.xlabel('time[seconds]')
  #pl.ylabel('power[w]')
  #pl.plot(N,p)
  #pl.show()
  return p

s1=on_off(60.0,60.0,1.0,66185,66192)
s2=on_off(1620.0,1600.0,0.0625,66193,66300)
s3=on_off(60.0,60.0,1.0,66301,66305)
s4=on_off(1620.0,1600.0,0.2,66306,66357)
s5=on_off(60.0,60.0,1.0,66358,66362)
s6=on_off(1620.0,1600.0,0.2,66363,66414)
s7=on_off(60.0,60.0,1.0,66415,66419)
s8=on_off(1620.0,1600.0,1.0,66420,66441)


for i in range(timeline):
  ss[i] = s1[i] + ss[i]
  ss[i] = s2[i] + ss[i]
  ss[i] = s3[i] + ss[i]
  ss[i] = s4[i] + ss[i]
  ss[i] = s5[i] + ss[i]
  ss[i] = s6[i] + ss[i]
  ss[i] = s7[i] + ss[i]
  ss[i] = s8[i] + ss[i]

print max(s2)
pl.xlim(66000,66500)
pl.ylim(0,1700)
pl.plot(ss)
pl.show()
