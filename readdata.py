import argparse
from calcplot import CalcPlot
global scale
import tool

tool.custom_rmdir("images")
ap = argparse.ArgumentParser()
ap.add_argument("-d","--dataset",required = True,help = "Path to dataset")
ap.add_argument("-r","--result",required = True,help = "Path to PDF")
ap.add_argument("-t","--test",required = True,type = bool,help = "test or experiment")
args = vars(ap.parse_args())

scale = {'SWANGLE':'°','SWTORQUE':'Nm','SPEED':'m/s','VELY':'m/s','FAACC':'m/s^2','LATACCRT':'m/s^2',
         'VERTACCL':'m/s^2','ROLLANGL':'°','PITCH':'°','YAWANGL':'°','ROLLRATE':'°/s','YAWVELRT':'°/s',
         'SIDESLIP':'°','MANEUVERID':'','TIME':'s','SWANGLEACC':'°/s2','SWTORQUE_COLUMN':'Nm'} 

datadict = tool.inputdata(args["dataset"],args["test"])     
calc1 = CalcPlot(datadict,scale)
(index0,index1,swa_state,t0,swa_middle) = calc1.calcSwa()
calc1.plotSwa(index0,index1,swa_middle)
dict1 = datadict.copy()
dict1.pop('TIME')
dict1.pop('SWANGLE')
for (key,value) in dict1.items():
    (index1,index2,peak,T_max,T_state,y_state) = calc1.calcOther(t0,key,index0)
    calc1.plotOther(index0,key,index1,index2,peak,T_max,T_state,y_state,swa_state)
tool.rpt(args["result"]+'.pdf')