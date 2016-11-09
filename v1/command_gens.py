'''--Designed For Day/Hour/Min/Sec Level randomly setting
   --Dong Chen 2015-05
'''
#!/usr/bin/python
import random
from random import randint
import csv
import math
import os

"clean logs and files"
output_file="quick_lib.csv"
if os.path.exists(output_file)==True:
  os.system(("rm -f ./%s")%(output_file))

def generateNumber(num):
    mylist = []
    for i in range(num+1):
         mylist.append(i)
    return mylist

def random_check(input_,loop_):
  #print input_
  input_temp = [input_[i] for i in range(len(input_)) if input_[i][0] > 0]
  if not input_temp:
    return [-1]
  #print input_temp
  input_temp_can = [100*input_[i][0] for i in range(len(input_)) if input_[i][0] > 0]
  input_temp_ret = [input_[i][1] for i in range(len(input_)) if input_[i][0] > 0]
  input_temp_can_final = [sum(input_temp_can[0:i+1]) for i in range(len(input_temp_can))]
  "set last item as 100 to sovle 99.99999 problem"
  input_temp_can_final[len(input_temp_can)-1] = 100
  #print input_temp_can_final
  ret_= random.sample(generateNumber(100),loop_)
  #print ret_
  output_ = []
  for r_ in range(len(ret_)):
    for i in range(len(input_temp_can_final)):
      if i != 0 and ret_[r_] <= input_temp_can_final[i] and ret_[r_] >input_temp_can_final[i-1]:
        output_.append(input_temp_ret[i]) 
      if i == 0 and ret_[r_] <= input_temp_can_final[i]:
        output_.append(input_temp_ret[i])
  return output_

a=[[0.1,0],[0.3,1],[0.2,9],[0,2],[0.4,23],[0,22]]

circuit_week_matrix = [[0 for x in range(7)] for x in range(25)] 
circuit_fre_matrix = [0]*25 
circuit_day_matrix = [[0 for x in range(24)] for x in range(25)] 
circuit_id = [0]*25
circuit_time = [0]*25

with open("configure.csv","r") as csvfile_xt:
  readfile=csv.reader(csvfile_xt,delimiter=',')
  x = 0
  for s in readfile:
    circuit_id[x] = int(s[0])
    circuit_time[x] = int(s[1])
    for i in range(7):
      circuit_week_matrix[x][i] = (float)(s[2+i])
    for j in range(24):
      circuit_day_matrix[x][j] = (float)(s[9+j])
    circuit_fre_matrix[x]=int(s[33])
    x = x + 1
  csvfile_xt.close()

#print circuit_week_matrix,circuit_day_matrix
input_circuit_week_matrix = [[] for x in xrange(25)]
input_circuit_day_matrix = [[] for x in xrange(25)]

for x in range(25):
  for i in range(7):
    "For testing only"
    input_circuit_week_matrix[x].append([circuit_week_matrix[x][i],i,circuit_fre_matrix[x]])
    #input_circuit_week_matrix[x].append([circuit_week_matrix[x][i],i,1])
for x in range(25):
  for i in range(24):
    input_circuit_day_matrix[x].append([circuit_day_matrix[x][i],i])

#print input_circuit_week_matrix

"Read modeling information"
"Parameters define"
Circuits=5000
Device_IDs=[0]*Circuits
Single_=[0]*Circuits
Device_names= ["" for xx in range(Circuits)]
model_type=[0]*Circuits
power_1_=[0]*Circuits
power_2_=[0]*Circuits
lamada_1_=[0]*Circuits
factor_=[0.0]*Circuits
background_=[0]*Circuits
device_num=0
counting=0
c_counting=0
last_id=0
timeline = 60*60*24*7

with open("device_model_mapping.csv","r") as csvfile_tx:
  readfile=csv.reader(csvfile_tx,delimiter=',')
  for s in readfile:
    Device_IDs[counting]=int(s[0])
    Single_[counting]=int(s[1])
    Device_names[counting]=str(s[2])
    model_type[counting]=int(s[3])
    power_1_[counting]=float(s[4])
    power_2_[counting]=float(s[5])
    lamada_1_[counting]=float(s[6])
    factor_[counting]=float(s[7])
    background_[counting]=int(s[8])
    counting=counting+1
    if Device_IDs[counting-1]!=last_id:
      c_counting=c_counting+1
    last_id=Device_IDs[counting-1]
csvfile_tx.close()
device_num=c_counting

#device max number 500
Dev_Max=500
Sub_num=50

"matrix keeping the model types and factors for sub-models"
Matrix = [[Dev_Max for x in range(Sub_num)] for x in range(Dev_Max)]
Matrix_ = [[Dev_Max for x in range(Sub_num)] for x in range(Dev_Max)]
Matrix_power_1_ = [[Dev_Max for x in range(Sub_num)] for x in range(Dev_Max)]
Matrix_power_2_ = [[Dev_Max for x in range(Sub_num)] for x in range(Dev_Max)]
Matrix_lamada_1_ = [[Dev_Max for x in range(Sub_num)] for x in range(Dev_Max)]
Matrix_background_= [[0 for x in range(Sub_num)] for x in range(Dev_Max)]
Final_id=[0]*Dev_Max

for i in range(0,counting):
  "solve the appliance starting from 0 problem"
  temp_dev=int(Device_IDs[i])-1
  #print temp_dev
  Final_id[temp_dev]=Final_id[temp_dev]+1
  #each device signature at lease can be divided into 8 sub traces
  for x in range(Sub_num):
    if Matrix[temp_dev][x]==Dev_Max:
       Matrix[temp_dev][x]=int(model_type[i])
       Matrix_[temp_dev][x]=factor_[i]
       Matrix_power_1_[temp_dev][x]=power_1_[i]
       Matrix_power_2_[temp_dev][x]=power_2_[i]
       Matrix_lamada_1_[temp_dev][x]=lamada_1_[i]
       Matrix_background_[temp_dev][x]=background_[i]
       #print Matrix_[temp_dev][x]
       #print Matrix_background_[temp_dev]
       break
#print Matrix[1],Matrix_[1]

def background_touch():
  print "background loading"
  return 1

for i in range(25):
  "Frequency is set by second item of the list of list data"
  day_cap = []
  hour_cap = []
  App_IDs = i + 1
  App_ID = i

  "add background check these circuits do not need randomly always on"
  if Matrix_background_[App_ID][0] >0:
    print "this is backgroud device"
    with open(output_file,"a") as csvfile_xxtt:
      writefile=csv.writer(csvfile_xxtt,delimiter=',')
      temp_t = 0
      duaration_tt = 0
      sub_len = 0
      for s in range(len(Matrix_background_[App_ID])):
        if Matrix_background_[App_ID][s] > 0:
          sub_len = sub_len +1
      #print sub_len
      to_end = 0
      inc_ = 0
      while to_end <= timeline:
        for l in range(sub_len):
          start_tt = temp_t
          #start_tt = temp_t + Matrix_background_[App_ID][0]*inc_
          #print sum(Matrix_[App_ID][0:l+1])
          duaration_tt = int(start_tt+Matrix_[App_ID][l])
          temp_t = duaration_tt + 1
          "Device,Model,P1,P2,P3,Start,End"
          #print start_tt,duaration_tt
          writefile.writerow([str(App_IDs),str(Matrix[int(App_ID)][l]),str(Matrix_power_1_[int(App_ID)][l]),str(Matrix_power_2_[int(App_ID)][l]),str(Matrix_lamada_1_[int(App_ID)][l]),start_tt,duaration_tt])
          to_end = duaration_tt + Matrix_background_[App_ID][0]
        inc_ = inc_ + 1
    csvfile_xxtt.close()
  else:
    print "testtest: "+str(input_circuit_week_matrix[i][2][2])
    if input_circuit_week_matrix[i][2][2]==0:
      with open(output_file,"a") as csvfile_xxtt:
        writefile=csv.writer(csvfile_xxtt,delimiter=',')
        "Device,Model,P1,P2,P3,Start,End"
        writefile.writerow([str(App_IDs),0,0,0,0,0,0])
      csvfile_xxtt.close()
      print "I got unactive circuit"
      continue
    "normally generate traces"
    "randomly on cirucits skipped from background circuits"
    for j in range(input_circuit_week_matrix[i][2][2]):
      t1=random_check(input_circuit_week_matrix[i],1)
      #if len(t1) != 0:
      if i == 17:
        print input_circuit_week_matrix[17]
      if t1:
        day_index = t1[0]
        t2=random_check(input_circuit_day_matrix[i],1)
        print "circuit-"+str(i+1)+", running on "
        day_cap.append(t1[0])
        hour_cap.append(t2[0])
    print day_cap,hour_cap
    for j in range(len(day_cap)):
      start_ = 24*60*60*j + hour_cap[j]*60*60 + random.randint(0,60*60)
      temp_circuit_time = random.uniform(0.9*circuit_time[i],1.1*circuit_time[i])
      print "different-"+str(temp_circuit_time)
      with open(output_file,"a") as csvfile_xxtt:
        writefile=csv.writer(csvfile_xxtt,delimiter=',')
        o_max=Final_id[int(App_ID)]
        "add random to spike appear times"
        #o_max=random.randint(1,o_max)
        print App_ID,o_max
        temp_ = start_
        duaration_t = 0
        for l in range(0,o_max):
          temp = Matrix_[int(App_ID)][0:l+1]
          start_t = temp_
          "add random for running time"
          duaration_t = int(start_+temp_circuit_time*60*sum(temp))
          temp_ = duaration_t + 1
          "Device,Model,P1,P2,P3,Start,End"
          #p1=random.uniform(0.9*Matrix_power_1_[int(App_ID)][l],1.1*Matrix_power_1_[int(App_ID)][l])
          #p2=random.uniform(0.9*Matrix_power_2_[int(App_ID)][l],1.1*Matrix_power_2_[int(App_ID)][l])
          writefile.writerow([str(App_IDs),str(Matrix[int(App_ID)][l]),str(Matrix_power_1_[int(App_ID)][l]),str(Matrix_power_2_[int(App_ID)][l]),str(Matrix_lamada_1_[int(App_ID)][l]),start_t,duaration_t])
          #writefile.writerow([str(App_IDs),str(Matrix[int(App_ID)][l]),str(p1),str(p2),str(Matrix_lamada_1_[int(App_ID)][l]),start_t,duaration_t])
      csvfile_xxtt.close()
