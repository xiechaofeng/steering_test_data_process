import argparse
from calcplot import CalcPlot
global scale
import tool

tool.custom_rmdir("images")
ap = argparse.ArgumentParser()
ap.add_argument("-dl","--datasetL",required = True,help = "Path to datasetL")
ap.add_argument("-dr","--datasetR",required = True,help = "Path to datasetR")
ap.add_argument("-r","--result",required = True,help = "Path to PDF")
ap.add_argument("-t","--test",required = True,type = bool,help = "test or experiment")
args = vars(ap.parse_args())

scale = {'SWANGLE':'°','SWTORQUE':'Nm','SPEED':'m/s','VELY':'m/s','FAACC':'m/s^2','LATACCRT':'m/s^2',
         'VERTACCL':'m/s^2','ROLLANGL':'°','PITCH':'°','YAWANGL':'°','ROLLRATE':'°/s','YAWVELRT':'°/s',
         'SIDESLIP':'°','MANEUVERID':'','TIME':'s','SWANGLEACC':'°/s2','SWTORQUE_COLUMN':'Nm'} 

datadictL = tool.inputdata(args["datasetL"],args["test"])     
calcL = CalcPlot(datadictL,scale)
(index0_L,index1_L,swa_state_L,t0_L,swa_middle_L) = calcL.calcSwa()
calcL.plotSwa(index0_L,index1_L,swa_middle_L)
dictL = datadictL.copy()
dictL.pop('TIME')
dictL.pop('SWANGLE')
datadictR = tool.inputdata(args["datasetR"],args["test"])     
calcR = CalcPlot(datadictR,scale)
(index0_R,index1_R,swa_state_R,t0_R,swa_middle_R) = calcR.calcSwa()
calcR.plotSwa(index0_R,index1_R,swa_middle_R)
dictR = datadictR.copy()
dictR.pop('TIME')
dictR.pop('SWANGLE')
for ((key_L,value_L),(key_R,value_R)) in zip(dictL.items(),dictR.items()):
    (index1_L,index2_L,peak_L,T_max_L,T_state_L,y_state_L) = calcL.calcOther(t0_L,key_L)
    (index1_R,index2_R,peak_R,T_max_R,T_state_R,y_state_R) = calcR.calcOther(t0_R,key_R)
    calcL.plotOther(index0_L,key_L,index1_L,index2_L,(peak_L+peak_R)/2.0,(T_max_L+T_max_R)/2.0,(T_state_L+T_state_R)/2.0,(y_state_L+y_state_R)/2.0,(swa_state_L+swa_state_R)/2.0)
tool.rpt(args["result"]+'.pdf')