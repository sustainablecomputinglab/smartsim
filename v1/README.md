# *SmartSim*: A Device Accurate Smart Home Simulator for Energy Analytics 

## Introduction

Utilities have deployed tens of millions of smart meters, which record and transmit home energy usage at fine- grained intervals. These deployments are motivating researchers to develop new energy analytics that mine smart meter data to learn insights into home energy usage and behavior. 

Unfortunately, a significant barrier to evaluating energy analytics is the overhead of instrumenting homes to collect aggregate energy usage data and data from each device. As a result, researchers typically evaluate their analytics on only a small number of homes, and cannot rigorously vary a home’s characteristics to determine what attributes of its energy usage affect accuracy. 

To address the problem, we develop SmartSim, a publicly-available device-accurate smart home energy trace generator. SmartSim generates energy usage traces for devices by combining a device energy model, which captures its pattern of energy usage when active, with a device usage model, which specifies its frequency, duration, and time of activity. SmartSim then generates aggregate energy data for a simulated home by combining the data from each device. We integrate SmartSim with NILM-TK, a publicly- available toolkit for Non-Intrusive Load Monitoring (NILM), and compare its synthetically generated traces with traces from a real home to show they yield similar quantitative and qualitative results for representative energy analytics.



<img src="https://cloud.githubusercontent.com/assets/6586953/19704718/c12d7a9c-9ad6-11e6-9e03-e83e1d552065.jpg" alt="Drawing" style="width: 80% height: 70%;"/>

## Current state of the project

The project is in its early stages. Please note that SmartSim is currently a research tool.

## Install

##### Install of SmartSim:

Please run the setup.py included in the sources.

##### Install of NILMTK:

Please refer to [NILMTK](https://github.com/nilmtk/nilmtk/blob/master/README.md) installation instructions page to install the NILMTK toolkit. 

After installation, please use "nosetests" command to test the correctness of NILMTK setup.

## Documents

Please go [Wiki](https://github.com/sustainablecomputinglab/smartsim/wiki) pages.



## Authors

*SmartSim: A Device-Accurate Smart Home Simulator for Energy Analytics.*, In Proceedings of *the 2016 IEEE International Conference on Smart Grid Communications (SmartGridComm),* Sydney, Australia, 2016.

*Dong Chen, David Irwin, Prashant Shenoy.* 