from celery import Celery
import json
from collections import Counter
import os
from sys import argv
import time
import uuid
import swiftclient.client    
import StringIO
import os
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

# file  being the file
def conv(file):
    tid = []
    lift = []
    drag = []
    
    f = open(file, "r")
    lines = f.readlines()

    for line in lines:
        line = line[:-2]
        tmp = line.split("\t")    
        lift.append(tmp[1])
        drag.append(tmp[2])
    f.close() 

    del lift[0]
    del drag[0]

    return([lift,drag])

def makePlot(data, Save):
    tmp = conv(data)
    data = tmp[0]

    N = len( data )
    x = np.arange(1, N+1)
    plt.plot(x,data)

    plt.savefig(Save + '/plot_lift.png')

    data = tmp[1]

    N = len( data )
    x = np.arange(1, N+1)
    plt.plot(x,data)
    #plt.savefig('plot_drag.png')
    plt.savefig(Save + '/plot_drag.png')

makePlot(argv[1], argv[2])
    
