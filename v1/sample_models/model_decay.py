#!/usr/bin/python
import math
import numpy as np
import pylab as pl

p_active=400
p_peak=450
lamada=0.04
NN=500
p=[0.0]*NN
N=[0]*NN
for j in range(1,NN+1):
  N[j-1]=j
for i in range(1,NN+1):
  p[i-1]=p_active+(p_peak-p_active)*math.exp(-lamada*i)
print N
print p
pl.xlim(1,NN)
pl.ylim(400,450)
pl.xlabel('t')
pl.ylabel('power')
pl.plot(N,p)
pl.show()
