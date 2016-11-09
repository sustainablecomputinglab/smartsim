#!/usr/bin/python
import math
import os
import numpy as np
import random
import matplotlib
matplotlib.use('PDF')
import csv
import matplotlib.pyplot as plt

M=50
file_list=[0]*M
file_flag=0

for file in os.listdir("./house_1"):
  if file.endswith(".dat"):
    file_list[file_flag]=file
    file_flag=file_flag+1

for file_flag in range(0,M-1):
  if file_list[file_flag]!=0 and file_list[file_flag]!="labels.dat":
    print file_list[file_flag]
    csvfile=open("./house_1/"+file_list[file_flag],"r")
    readfile=csv.reader(csvfile,delimiter=' ')
    dump=0
    output_0=[0]*1440*1*60*7
    output_1=[0.0]*1440*1*60*7
    output_index=0
    #pickup the target appliance trace
    for line in readfile:
      r=list(line)
      output_0[output_index]=r[0]
      output_1[output_index]=r[1]
      dump=dump+1
      output_index=output_index+1
    #plt.ylim(0,14000)
    #plt.xlim(0,1440*60*7)
    #plt.xlim(70000,80000)
    plt.xlabel('time[seconds]')
    plt.ylabel('power[w]')
    plt.plot(output_0,output_1)
    target_file="%s.pdf"%("./house_1/"+file_list[file_flag])
    plt.savefig(target_file)
    plt.close()
    csvfile.close()
