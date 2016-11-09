#!/usr/bin/python
import math
import csv
import os
import random 

Circuits=500
Device_IDs=[0]*Circuits
Single_=[0]*Circuits
Device_names= ["" for xx in range(Circuits)]
model_type=[0]*Circuits
power_1_=[0]*Circuits
power_2_=[0]*Circuits
lamada_1_=[0]*Circuits
factor_=[0]*Circuits
device_num=0
counting=0
c_counting=0
last_id=0


with open("device_model_mapping.csv","r") as csvfile_tx:
  readfile=csv.reader(csvfile_tx,delimiter=',')
  for s in readfile:
    Device_IDs[counting]=int(s[0])
    Single_[counting]=int(s[1])
    Device_names[counting]=str(s[2])
    model_type[counting]=(s[3])
    power_1_[counting]=float(s[4])
    power_2_[counting]=float(s[5])
    lamada_1_[counting]=float(s[6])
    factor_[counting]=float(s[7])
    counting=counting+1
    if Device_IDs[counting]!=last_id:
      c_counting=c_counting+1
    last_id=Device_IDs[counting]
csvfile_tx.close()
device_num=c_counting
print device_num,Device_names

#device max number 500
Dev_Max=500
Final_id=[0]*Dev_Max
Matrix = [[Dev_Max for x in range(8)] for x in range(Dev_Max)]
for i in range(0,counting):
  temp_dev=int(Device_IDs[i])
  print temp_dev
  Final_id[temp_dev]=Final_id[temp_dev]+1
  #each device signature at lease can be divided into 8 sub traces
  for x in range(0,8):
    if Matrix[temp_dev][x]==Dev_Max:
       Matrix[temp_dev][x]=int(model_type[i])
       break
print Final_id
print Matrix

with open("configure.csv","r") as csvfile_xt:
  readfile=csv.reader(csvfile_xt,delimiter=',')
  for s in readfile:
    week_p=[0]*7
    day_p=[0]*24
    App_ID=0
    Dua_=0
    #reading on..
    App_ID=s[0]
    Dua_=(int)(s[1])
    for i in range(7):
      week_p[i]=(float)(s[2+i])
      week_p[i]=round(7*week_p[i])
    for j in range(23):
      day_p[j]=(float)(s[9+j])
      day_p[j]=round(7*day_p[j])
    #print week_p
    #print day_p
    for day_ in range(7):
      hour_=25
      for time_ in range(24):
         if day_p[time_]>0:
           day_p[time_]=day_p[time_]-1
           hour_=time_
           print "1-done",hour_
           print "1-done",day_
           stamp_control_s=0
           stamp_control_e=1440*60
           start_=0
           duaration_=0
           #set random start second
           def pickup():
             return random.randint(0,60*60)
           #set random duration
           start_=1440*60*day_+hour_*60*60+pickup()
           duaration_=start_+Dua_
           output_file="quick_lib.csv"
           with open(output_file,"a") as csvfile_xxtt:
             writefile=csv.writer(csvfile_xxtt,delimiter=',')
             o_max=Final_id[int(App_ID)]
             for l in range(0,o_max):
               #c-out-appliance_id-model-start-running time
               writefile.writerow(["Device-"+str(App_ID),"Model-"+str(Matrix[int(App_ID)][l]),start_,duaration_])
               #print str(Matrix[int(App_ID)][l])
           csvfile_xxtt.close()
csvfile_xt.close()
