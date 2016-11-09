#!/usr/bin/python
import math
import numpy as np
import pylab as pl
import random
import csv
import os
from operator import add

"clean traces folder cache"
os.system("rm -rf ./house_1/")
current_=os.path.dirname(os.path.abspath(__file__))

"(Max#-1) devices for 1 day second level trace"
Circuits=10000
timeline=60*60*24*7

model={}
model[0]='on_off'
model[1]='decay'
model[2]='decay_grow'
model[3]='min_max'
model[4]='random_range'

"read from configure file"
start_=[0]*Circuits
end_=[0]*Circuits
Device_IDs=[0]*Circuits
Device_IDs_=[0]*Circuits
Device_names= ["" for xx in range(Circuits)]
model_type=[0]*Circuits
power_1_=[0]*Circuits
power_2_=[0]*Circuits
lamada_1_=[0]*Circuits
start_time=[0]*Circuits
end_time=[0]*Circuits
device_num=0
counting=0
counting_=0
c_counting=0
last_id=0

#with open("device_mapping.csv","r") as csvfile_tx:
#  readfile=csv.reader(csvfile_tx,delimiter=',')
#  device_num=sum(1 for s in readfile)
#csvfile_tx.close()

with open("device_model_mapping.csv","r") as csvfile_tx:
  readfile=csv.reader(csvfile_tx,delimiter=',')
  for s in readfile:
    Device_IDs_[counting_]=int(s[0])
    Device_names[counting_]=str(s[2])
    counting_ = counting_ + 1
csvfile_tx.close()


with open("./quick_lib.csv","r") as csvfile_tx:
  readfile=csv.reader(csvfile_tx,delimiter=',')
  for s in readfile:
    #print counting
    Device_IDs[counting]=int(s[0])
    model_type[counting]=int(s[1])
    power_1_[counting]=float(s[2])
    power_2_[counting]=float(s[3])
    lamada_1_[counting]=float(s[4])
    start_time[counting]=int(s[5])
    end_time[counting]=int(s[6])
    if Device_IDs[counting]!=last_id:
      c_counting=c_counting+1
    last_id=Device_IDs[counting]
    counting=counting+1
csvfile_tx.close()
device_num=counting

#print device_num

command_line="Generating ... #%d devices for 1 week second level trace"%device_num
print command_line

def on_off(s_t,e_t,p_ON_t,p_OFF_t,lamada_):
  p_ON,p_OFF=p_ON_t,p_OFF_t
  s,e=s_t,e_t
  NN=e-s+1
  p=[0.0]*timeline
  for i in range(s,e):
    p[i]=p_OFF
  to_stop = s+int(NN*(1-lamada_))
  for i in range(s,to_stop):
    p[i]=p_ON
  return p

def decay(s_t,e_t,p_peak_,p_active_,lamada_):
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

def decay_grow(s_t,e_t,p_base_,p_none_,lamda_):
  "Basic Decay Growth Model"
  s,e=s_t,e_t
  p_base,lamda=p_base_,lamda_
  NN=e-s+1
  p=[0.0]*timeline
  N=[0]*timeline
  for j in range(1,timeline+1):
    N[j-1]=j
  for i in range(1,NN+1):
    if s+i-1<=timeline:
      p[s+i-1]=p_base+lamda*math.log(i)
  #pl.xlim(1,timeline)
  #pl.ylim(1800,2500)
  #pl.xlabel('t')
  #pl.ylabel('power')
  #pl.plot(N,p)
  #pl.show()
  return p

def min_max(s_t,e_t,p_active_t,p_spike_t,lamda_t):
  s,e=s_t,e_t
  p_active,p_spike=p_active_t,p_spike_t
  lamda=1.0/lamda_t
  NN=e-s+1
  p=[0]*timeline
  p_=[0]*timeline
  N=[0]*timeline
  for i in range(0,timeline):
    N[i]=i+1
  check=[random.expovariate(lamda) for i in range(NN)]
  p_[0]=1
  for j in range(0,NN):
    bounder=int(sum(check[0:j]))
    if bounder<NN:
      p_[bounder]=1
  for i in range(0,NN):
    if s+i<timeline:
      if p_[i]==1:
        p[s+i]=random.randint((p_active-p_spike),p_active)
      else:
        p[s+i]=p_active
  #print check
  #pl.xlim(0,timeline)
  #pl.ylim(0,380)
  #pl.xlabel('t')
  #pl.ylabel('power')
  #pl.plot(N,p)
  #pl.show()
  return p

def random_range(s_t,e_t,p_max,p_min,lamada):
  s,e=s_t,e_t
  p_max,p_min=p_max,p_min
  p=[0]*timeline
  NN=e-s+1
  N=[0]*timeline
  for i in range(0,timeline):
    N[i]=i+1
  for i in range(0,NN):
    if s+i <timeline:
      p[s+i]=random.randint(p_min,p_max)
  #pl.xlim(0,timeline)
  #pl.ylim(0,1500)
  #pl.xlabel('t')
  #pl.ylabel('power')
  #pl.plot(N,p)
  #pl.show()
  return p

#device_={}
#device_dump={}
device_= [[0.0]*timeline for x in xrange(device_num)]
#print len(device_)
command={}
circuit_num=0

"make model name can run as command"
for circuit_num in range(0,device_num):
  #print "xxx"+str(circuit_num)
  command[circuit_num]=model[model_type[circuit_num]]+'(%d,%d,%d,%d,%f)'%(start_time[circuit_num],end_time[circuit_num],power_1_[circuit_num],power_2_[circuit_num],lamada_1_[circuit_num])
  device_[circuit_num]=eval(command[circuit_num])
  #print max(device_[circuit_num])
  #print command

#print max(device_[0]),200
"-1- dump trace for each circuit/device"
#time_start=1421423141
time_start=0

"all the sub-circuits belong the same appliance should be dump together"
#for circuit_num in range(0,max(Device_IDs)):
#  device_dump[circuit_num]=[0.0]*timeline
device_dump = [[0.0]*timeline for x in xrange(max(Device_IDs))]
last_device=-1
last_tracker=0
c=0
for circuit_num in range(device_num):
  #print max(device_[circuit_num]),100
  if Device_IDs[circuit_num]!=last_device:
    mult_=0
    last_tracker=last_tracker+1
    c=c+1
    #print "c"+str(c)+" "+str(len(device_dump))
    #print (device_dump[last_tracker-1]),(device_[circuit_num]) 
    device_dump[last_tracker-1]=map(add,device_dump[last_tracker-1],device_[circuit_num])
    #device_dump[last_tracker-1]=map(add,device_dump[last_tracker-1],device_[circuit_num])
    #print Device_IDs
  else:
    mult_=mult_+1
    #print "subtraces: "+str(mult_)+"of device "+str(last_tracker)+"total:"+str(len(device_dump))
    #print max(device_dump[last_tracker-1]),max(device_[circuit_num]) 
    device_dump[last_tracker-1]=map(add,device_dump[last_tracker-1],device_[circuit_num])
    #for length_ in range(0,timeline):
    #  device_dump[last_tracker-1][length_]=device_dump[last_tracker-1][length_]+device_[circuit_num][length_]
  last_device=Device_IDs[circuit_num]
  #del device_[circuit_num]
  #print sum(device_[circuit_num])

for circuit_num in range(0,max(Device_IDs)):
  "channel 1 and 2 are used for HDF5 metadata"
  file_=current_+"/house_1/channel_%d.dat" %(circuit_num+3)
  if not os.path.exists(os.path.dirname(file_)):
    os.makedirs(os.path.dirname(file_))
  with open(file_,"w") as csvfile_:
    writefile=csv.writer(csvfile_,delimiter=' ')
    for j in range(0,timeline):
      "add 1% meter reading error all circuits"
      final_power = random.uniform(0.99*device_dump[circuit_num][j],1.01*device_dump[circuit_num][j])
      writefile.writerow([j+time_start,final_power])
      #writefile.writerow([j+time_start,device_dump[circuit_num][j]])
  csvfile_.close()
  #print sum(device_dump[circuit_num])/60/60/7

"-2- dump total power usage trace"
for _hd in range(2):
  file_t=current_+"/house_1/channel_%d.dat" %(_hd+1)
  total_power=[0.0]*timeline
  #print "device_num"+str(device_num)
  for i in range(0,max(Device_IDs)):
    for j in range(0,timeline):
      total_power[j]=total_power[j]+device_dump[i][j]
  if not os.path.exists(os.path.dirname(file_t)):
    os.makedirs(os.path.dirname(file_t))
  with open(file_t,"w") as csvfile_t:
    writefile=csv.writer(csvfile_t,delimiter=' ')
    for j in range(0,timeline):
      writefile.writerow([j+time_start,total_power[j]])
  csvfile_t.close()
  #print sum(total_power)/60/60/7

"-3- dump circuit labels"
Last_ID=0
new_index=1
file_xt=current_+"/house_1/labels.dat"
if not os.path.exists(os.path.dirname(file_xt)):
  os.makedirs(os.path.dirname(file_xt))
with open(file_xt,"w") as csvfile_xt:
  writefile=csv.writer(csvfile_xt,delimiter=' ')
  for _in in range(0,2):
    writefile.writerow([new_index,"mains"])
    new_index=new_index+1
  #print device_num,new_index
  for s in range(0,counting_):
    if Device_IDs_[s]!=Last_ID:
      writefile.writerow([new_index,Device_names[s]])
      Last_ID=Device_IDs_[s]
      #print new_index
      new_index=new_index+1
csvfile_xt.close()
