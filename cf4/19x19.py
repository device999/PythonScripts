import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import time
from Tkinter import *


def  graphStart():
    root=Tk()
    column_coord=np.array([50,77,104,131,158,185,212,239,266,293,320,347,374,401,428,455,482,509,536,563])
    line_coord= np.array([75,102,129,156,183,210,237,264,291,318,345,372,399,426,453,480,507,534,561,588])
    text_coord=np.array([67,90,121,145,170,197,227,253,279,305,330,358,388,410,440,470,500,525,550,580])
    canvas=Canvas(root,width=1200,height=1200)
    canvas.pack(fill=BOTH)
    z=0
    i=0
    for element  in column_coord:
        canvas.create_line(column_coord[i],75,column_coord[i],588,fill="black")
        i =i+1
    j=0
    for elem in  line_coord:
        canvas.create_line(50,line_coord[j],564,line_coord[j],fill="black")
        j=j+1
    z=0
    for el in text_coord:
        canvas.create_text(text_coord[z],65,text=str(z))
        z=z+1
    z=0
    line_in=0
    column_in=0
    x_in=50
    y_in=75

    for line_in in range(19):
        for column_in in range(19):
                canvas.create_oval(x_in+column_in*27,y_in+line_in*27,x_in+(column_in*27)+27,y_in+(line_in*27)+27,fill= "lime")

    root.mainloop()

if __name__ == '__main__':
    graphStart()
