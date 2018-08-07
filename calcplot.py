import numpy as np
import matplotlib.pyplot as plt
global tendindex
from scipy.interpolate import interp1d

tend = 4.0
deltat = 0.01
tendindex = int(tend/deltat)
class CalcPlot:
    def __init__(self,datadict,scale):
        self.datadict = datadict
        self.scale = scale
        
    def calcSwa(self):
        time = self.datadict['TIME'][:tendindex]
        swa = self.datadict['SWANGLE'][:tendindex]
        index = np.argsort(np.diff(np.diff(swa[:200])))
        f = interp1d(time[index[-1]:index[0]+1],swa[index[-1]:index[0]+1],kind='linear')
        time_pred=np.linspace(time[index[-1]],time[index[0]],num=200)
        swa_pred = f(time_pred)
        swa_state = np.mean(swa[tendindex-200:tendindex])
        swa_state0 = np.mean(swa[0:index[-1]])
        swa_middle = (swa_state+swa_state0) / 2.0
        t0 = time_pred[np.argmin(np.abs(swa_pred-swa_middle))]
        index0 = np.argmin(np.abs(time-t0))
        index1 = np.argmin(np.abs(swa-swa_state))
        return (index0,index1,swa_state,t0,swa_middle)
    
    def plotSwa(self,index0,index1,swa_middle):
        swa = self.datadict['SWANGLE'][:tendindex]
        time = self.datadict['TIME'][:tendindex]
        swa_state = swa[index1]
        plt.figure(figsize=(10*3,10), dpi=300)
        plt.plot(time,swa,lineWidth = 4.0)
        plt.plot(time[index0],swa[index0],'o',markersize=10)
        plt.plot(np.array([time[index0],time[index0]]),np.array([swa[0],swa[index0]]),':',lw = 4.0,color='g')
        plt.plot(np.array([time[0],time[index0]]),np.array([swa[index0],swa[index0]]),':',lw = 4.0,color='g')
        plt.plot(np.array([time[0],time[index1]]),np.array([swa_state,swa_state]),':',lw = 4.0,color='g')
        plt.annotate('(%.2f,%.2f)' % (time[index0],swa_middle), xy=(time[index0],swa[index0]), xytext=(time[index0-30],swa[index0]*1.01),fontsize = 18)
        plt.annotate('(%.2f)' % (swa[index1]), xy=(time[index0],swa[index1]), xytext=(time[index0],swa[index1]*1.05),fontsize = 18)
        plt.title('SWANGLE',fontsize = 22)
        ax = plt.gca()
        ax.spines['top'].set_color(None) 
        ax.spines['right'].set_color(None) 
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.set_xlabel('%s/%s' % ('TIME',self.scale['TIME']),fontsize = 20)
        ax.set_ylabel('SWANGLE/%s' % self.scale['SWANGLE'],fontsize = 20)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.savefig('images/SWANGLE.jpg')
        plt.close()
        
    def calcOther(self,t0,name,index0):
        time = self.datadict['TIME'][:tendindex]
        if name in ['ROLLANGL','SIDESLIP','VELY','VERTACCL','ROLLRATE']:
            y = -self.datadict[name][:tendindex]
        else:
            y = self.datadict[name][:tendindex]
        index1 = np.argmin(abs(np.diff(y[index0+10:index0+90])))+index0+10
        index1 = np.argmax(y[:index1+1])
        y_state = np.mean(y[tendindex-150:tendindex])
        peak = y[index1] - y_state
        T_max = time[index1] - t0
        index2 = np.argmin(np.abs(y[:index1]-0.9*y_state))
        T_state = time[index2] - t0
        return (index1,index2,peak,T_max,T_state,y_state)
    
    def plotOther(self,index0,name,index1,index2,peak,T_max,T_state,y_state,swa_state):
        t = self.datadict['TIME'][:tendindex]
        y = self.datadict[name][:tendindex]
        if name in ['ROLLANGL','SIDESLIP','VELY','VERTACCL','ROLLRATE']:
            y_state = -y_state
            peak = -peak
        plt.figure(figsize=(10*3,10), dpi=300)
        plt.plot(t,y,lineWidth = 4.0)
        plt.plot(t[index1],y[index1],'o',t[index2],y[index2],'o',t[index0],y[index0],'o',markersize=10)
        plt.plot(np.array([t[index0],t[index0]]),np.array([y[0],y[index0]]),':',lw = 4.0,color='g')
        plt.plot(np.array([t[index2],t[index2]]),np.array([y[0],y[index2]]),':',lw = 4.0,color='g')
        plt.plot(np.array([t[index1],t[index1]]),np.array([y[0],y[index1]]),':',lw = 4.0,color='g')
        plt.plot(np.array([t[index2],t[-10]]),np.array([y[index2],y[index2]]),':',lw = 4.0,color='g')
        plt.plot(np.array([t[0],t[-10]]),np.array([y_state,y_state]),':',lw = 4.0,color='g')
        plt.plot(np.array([t[0],t[index1]]),np.array([y[index1],y[index1]]),':',lw = 4.0,color='g')
        plt.annotate('(%.2f,%.2f)' % (t[index0],y[index0]), xy=(t[index0],y[index0]), xytext=(t[index0-30],y[index0]),fontsize = 18)
        plt.annotate('(%.2f,%.2f)' % (t[index2],y[index2]), xy=(t[index2],y[index2]), xytext=(t[index2-30],y[index2]),fontsize = 18)
        plt.annotate('(%.2f,%.2f)' % (t[index1],y[index1]), xy=(t[index1],y[index1]), xytext=(t[index1-30],y[index1]*1.05),fontsize = 18)
        plt.annotate('(%.2f)' % (y_state), xy=(t[-50],y_state), xytext=(t[-50],y_state*1.05),fontsize = 16)
        plt.annotate('(%.2f)' % (y[index2]), xy=(t[-50],y[index2]), xytext=(t[-50],y[index2]*1.05),fontsize = 16)
        if name == 'YAWVELRT':
            plt.text(t[-150],(y[0]+y[-1])*0.6,'response time = %.3f s\npeak response time = %.3f s\novershootvalue = %.3f %s\nSteady-state yaw velocity response gain = %.3f s-1' % (T_state,T_max,peak,self.scale[name],y_state/swa_state),fontsize = 18)
        else:
            plt.text(t[-150],(y[0]+y[-1])*0.6,'response time = %.3f s\npeak response time = %.3f s\novershootvalue = %.3f %s' % (T_state,T_max,peak,self.scale[name]),fontsize = 18)
        ax = plt.gca()
        ax.spines['top'].set_color(None)
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['right'].set_color(None) 
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))
        ax.spines['left'].set_linewidth(2)  
        ax.set_xlabel('%s/%s' % ('TIME',self.scale['TIME']),fontsize = 20)
        ax.set_ylabel('%s/%s' % (name,self.scale[name]),fontsize = 20)
        plt.title(name,fontsize = 22,verticalalignment='top')
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.savefig('images/%s.jpg' % name)
        plt.close()
        