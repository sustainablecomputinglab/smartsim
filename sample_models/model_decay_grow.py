#!/usr/bin/python
import math
import numpy as np
import pylab as pl

p_base=400
lamda=40
NN=80
p=[0.0]*NN
N=[0]*NN
for j in range(1,NN+1):
  N[j-1]=j
for i in range(1,NN+1):
  p[i-1]=p_base+lamda*math.log(i)
print N
print p
pl.xlim(1,500)
pl.ylim(400,1500)
pl.xlabel('t')
pl.ylabel('power')
pl.plot(N,p)
pl.show()
