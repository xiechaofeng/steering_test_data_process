from reportlab.platypus import SimpleDocTemplate,Image,Table,TableStyle
import time
import glob
import os
import re
import numpy as np
from scipy import signal

def custom_rmdir(path):
    if len(os.listdir(path)): 
        for sub_name in os.listdir(path):
            sub_path = os.path.join(path, sub_name)
            if os.path.isfile(sub_path):
                os.remove(sub_path)

def inputdata(dataset,test):
    orientation = dataset[-1]
    deltat = 0.01
    with open(dataset,"r") as f:
        file = f.read()
        pattern = re.compile(r'=.*?([a-zA-Z]+_?[a-zA-Z]+)')
        channels = re.findall(pattern, file)
        pattern = re.compile(r'TIME: (.*?) sec     DATE: (.*?)    HOUR: (.*?)    ID: (.*?)\n')
        total = re.findall(pattern,file)
        f.close()
    with open(dataset,"r") as f:
        lines = f.readlines()
        index = []
        for (i,line) in enumerate(lines):
            if 'HOUR' in line:
                index.append(i+3)
    Total = []
    TEND = []
    for ((TIME,DATE,HOUR,ID),INDEX) in zip(total,index):
        TEND.append(float(TIME))
        Total.append((INDEX,float(TIME),DATE.strip()+' '+HOUR.strip(),ID.strip()))
    tend = min(TEND)
    DATA = np.zeros((int(tend/deltat)+1,len(channels)))
    for (INDEX,TIME,_,_) in Total:
        data = []
        for line in lines[INDEX:(INDEX+int(tend/deltat)+1)]:
            d = [float(x) for x in line.split()]
            data.append(d)
        DATA += np.array(data)
    DATA = DATA / float(len(Total))
    datadict = {}
    for (i,name) in enumerate(channels):
        if name in ['SWANGLE','LATACCRT','ROLLANGL','YAWVELRT','SIDESLIP']:
            if orientation.lower() == 'l' and name not in ['SPEED','FAACC','VERTACCL','PITCH']:
                datadict[name] = -DATA[:,i]
            else:
                datadict[name] = DATA[:,i]
    t = np.arange(0,TIME+deltat,deltat)
    datadict['TIME'] = t
    
    if test:
        b, a = signal.cheby1(4,0.05,3.5/(0.5/deltat))
        for (name,value) in datadict.items():
            if name in ['TIME','SWANGLE']:
                continue
            value = signal.filtfilt(b,a,value)
            datadict[name] = value 
    return datadict

def rpt(name):
    story=[]
    height = 200
    width = 200*3

    curr_date = time.strftime("%Y-%m-%d", time.localtime())
    component_data = [['Test report--Presentation of results: %s' % curr_date]]
    for imagePath in glob.glob('images/*.jpg'):
        img0 = Image(imagePath)
        img0.drawHeight = height
        img0.drawWidth = width
        component_data.append([img0])

    component_table = Table(component_data, colWidths=[width])
    component_table.setStyle(TableStyle([
    ('FONTSIZE',(0,1),(-1,-1),10),
    ('VALIGN',(-1,0),(-1,-1),'TOP'),  
    ('ALIGN',(-1,0),(-1,-1),'CENTER'), 
    ]))
    story.append(component_table)
    doc = SimpleDocTemplate(name)
    doc.build(story)  