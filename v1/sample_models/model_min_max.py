#!/usr/bin/python
import math
import random
import numpy as np
import pylab as pl

p_active=160
p_spike=120
lamda=1.0/10.82
NN=5000
p=[0]*NN
p_=[0]*NN
N=[0]*NN

for i in range(0,NN):
  N[i]=i+1

check=[random.expovariate(lamda) for i in range(NN)]

p_[0]=1
for j in range(0,NN):
  bounder=int(sum(check[0:j]))
  if bounder<NN:
    p_[bounder]=1

#for i in range(0,NN):
#  for j in range(0,NN):
#    if int(sum(check[0:j]))==i:
#      p_[i]=1
for i in range(0,NN):
  if p_[i]==1:
    p[i]=random.randint((p_active-p_spike),p_active)
  else:
    p[i]=p_active
    
print check
#pl.xlim(0,NN)
pl.ylim(0,170)
pl.xlabel('t')
pl.ylabel('power')
pl.plot(N,p)
pl.show()
