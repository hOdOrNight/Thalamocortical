#!/usr/bin/env python

# For documentation of this script please see print message when run with -help
# And note inline comments that explain what to customise to run on a different platform / setup

# matplotlib is available for Linux, Mac and Windows from http://matplotlib.sourceforge.net

import sys
import os
import inspect
import time
import math
import shlex
import subprocess
import datetime
import re

import matplotlib.pyplot as plt
from pylab import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# defaults set
debugFlag = 0
helpFlag = 0
showFlag = 0
overlayFlag = 0
alphaFlag = 0
dtFlag = 0
dtfileFlag = 0
dtfileParams = []
windowFlag = 0
windowParams = []
xlabelFlag = 0
ylabelFlag = 0
glabelFlag = 0
targetList = []
arg_parms = []

xlabelParams = "X-Label Title (units)"
ylabelParams = "Y-Label Title (units)"
glabelParams = "G-Label Title (units)"

#  ./plotDat.py -win:'0,-80,500,120' -xlabel:'hello there' -ylabel:'my friend' -glabel:'hi there graph' -alpha batchdata/batchdata_v_2012-05-25_1814-29.dat 


for arg in sys.argv:
    # handle parameters with options like -win:'n,n,n,n'
    if (arg.count(":")):
        arg_parms = arg.split(":",2)
        arg = arg_parms[0].strip("'")        
        
    if (arg == "-dt"):
        dtFlag = 1
        dtParams = arg_parms[1]
    if (arg == "-win"):
        windowFlag = 1
        windowParams = arg_parms[1].split(",",4)
    if (arg == "-xlabel"):
        xlabelFlag = 1
        xlabelParams = arg_parms[1].replace("_"," ")
    if (arg == "-ylabel"):
        ylabelFlag = 1
        ylabelParams = arg_parms[1].replace("_"," ")
    if (arg == "-glabel"):
        glabelFlag = 1
        glabelParams = arg_parms[1].replace("_"," ")
    if (arg == "-dtfile"):
        dtfileFlag = 1
        dtfileParams = arg_parms[1]
    if (arg == "-debug"):
        DEBUG = True
        debugFlag = 1
    if (arg == "-help"):
        helpFlag = 1
    if (arg == "-show"):
        showFlag = 1
    if (arg == "-alpha"):
        alphaFlag = 1
    if (arg == "-overlay"):
        overlayFlag = 1
    if (len(arg) > 1 and arg[0] != "-" and arg.count(".py") == 0):
        # file location argument
        targetList.append(arg)
        print "target queued: "+arg

if (helpFlag == 1):
    print "Call this script as follows: -- need to update -- \n\
    ./plotDat.py [options] <file1> <file2> <file3> ...  \n\
    -debug to debug and not do anything\n\
    -show to show \n\
    -alpha to draw background transparent \n\
    -overlay to draw multiple files on one graph as overlay \n\
    -help for this text \n\
    -dtfile:filename\n\
    -win:<minx,miny,maxx,maxy> to control output range \n\
    -xlabel:'<text_on_xlabel>'\n\
    -ylabel:'<text_on_ylabel>'\n\
    -glabel:'<text_on_glabel> text on graph overall'\n\
    \n\
    NOTE: the script is not 100% stable, some combinations do not work\n\
    \n"
    quit()

#    -type=nm for neuromatic folders \n\
#    -type=nc for neuroconstruct folders \n\

 
DEBUG = True
def debugPrint(prStr):
    if (DEBUG):
        _, filename, linenumber, _, _, _ = inspect.stack()[1]
        print filename+" lineno:"+str(linenumber)+" : "+prStr
        

plotNum = 0

plotcolors=['#000000','#550000','#005500','#000055', \
            '#555555','#880000','#008800','#000088', \
            '#888888','#990000','#009900','#000099', \
]


# for each file sent as argument create a plot
for filidx in range(0,len(targetList)):
    targetFile = targetList[filidx]
    # read the x values
    if (os.path.exists(targetFile) ):
        # read the y values
        data_y = []
        data_x = []
        t = 0
        if (dtfileFlag and os.path.exists(dtfileParams)):
            file_x = open(dtfileParams,'rU')
            debugPrint("Reading X vals from file:"+dtfileParams)
            for line in file_x:
                if not line.strip().startswith('#') or not line.strip():
                    try:
                        data = float(line)
                        data_x.append(data)
                    except:
                        debugPrint("skipping line (bad format):"+str(line))
                        continue
            file_x.close()

        else:
            if (dtFlag):
                dt = float(dtParams)
            else:
                dt = 1
        file_y = open(targetFile,'rU')
        debugPrint("Reading file:"+targetFile)
        for line in file_y:
            if not line.strip().startswith('#') or not line.strip():
                try:
                    data = float(line)
                    data_y.append(data)
                    if (not dtfileFlag):
                        data_x.append(t)
                        t=t+dt
                except:
                    debugPrint("skipping line (bad format):"+str(line))
                    continue
                
        file_y.close()                    
        debugPrint("imported last data dat_y:"+str(data)+" records: "+str(t))
        # !! need to check for size differences in dimension

        if (overlayFlag == 0):
            fig = plt.figure(facecolor='#FFFFFF', edgecolor='#FFFFFF')
            if (windowFlag):
                ax = fig.add_subplot(111, autoscale_on=False, frame_on=True)
                ax.axis([int(windowParams[0]),int(windowParams[2]), int(windowParams[1]),int(windowParams[3])])
            else:
                ax = fig.add_subplot(111, autoscale_on=True, frame_on=True)
            #fig = plt.figure()
            fig.patch.set_alpha(0.0)
            #ax = fig.add_subplot(111)
            ax.patch.set_alpha(0.0)
            # should have a flag for alpha?            
            ax.spines['top'].set_color('none')
            ax.spines['right'].set_color('none')
            #    ax.plot(data_x, data_y, color='#000000', linestyle='None', solid_joinstyle ='round', solid_capstyle ='round',  marker='o', markerfacecolor='None', markeredgecolor='#000000' )
            #ax.plot(data_x, data_y, color='#000000', linestyle='None', solid_joinstyle ='round', solid_capstyle ='round',  marker=',', markerfacecolor='None', markeredgecolor='#000000' )
            ax.plot(data_x, data_y, color='#000000', linestyle='-', marker=',', markerfacecolor='None', markeredgecolor='#000000' )
            if (glabelFlag):
                ttl1 = title(glabelParams)
            else:
                title('Plot of file: '+targetFile)
            ttl1xy = ttl1.get_position()
            ttl1.set_position([ttl1xy[0],ttl1xy[1]+0.03])
            ax.set_ylabel(ylabelParams, fontsize=14)
            ax.set_xlabel(xlabelParams, fontsize=14)
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            # draw()
            canvas = FigureCanvas(fig)
            graphicsFilename = targetFile
            graphicsFilename = graphicsFilename.replace('.txt','')
            #canvas.print_eps(graphicsFilename+'.eps')
            #canvas.print_pdf(graphicsFilename+'.pdf')
            canvas.print_png(graphicsFilename+'.png')
            plt.close(fig)
            
        else:
            if (plotNum == 0):
                debugPrint("creating plot...")
                fig = plt.figure(facecolor='#FFFFFF', edgecolor='#FFFFFF')
                ax = fig.add_subplot(111, autoscale_on=True, frame_on=True)
                ax.spines['top'].set_color('none')
                ax.spines['right'].set_color('none')
                title(glabelParams)
                ax.set_ylabel(ylabelParams, fontsize=14)
                ax.set_xlabel(xlabelParams, fontsize=14)
                ax.xaxis.set_ticks_position('bottom')
                ax.yaxis.set_ticks_position('left')
            #    ax.plot(data_x, data_y, color='#000000', linestyle='None', solid_joinstyle ='round', solid_capstyle ='round',  marker='o', markerfacecolor='None', markeredgecolor='#000000' )
            #ax.plot(data_x, data_y, color='#000000', linestyle='None', solid_joinstyle ='round', solid_capstyle ='round',  marker=',', markerfacecolor='None', markeredgecolor='#000000' )
            debugPrint("plotting data_x data_y")
            ax.plot(data_x, data_y, color=plotcolors[plotNum % len(plotcolors)], linestyle='-', marker=',', markerfacecolor='None', markeredgecolor='#000000' )
            plotNum += 1
            

if (showFlag == 1):
    # show graphs for a certain amount of time then exit
    plt.show(1) # pass 0 to show and move on - 1 blocks and waits
    time.sleep(6)

# can I lay out the windows for the graphs or better to consolidate all sources in one graph?
# the idea is to create a workflow while I an working in neuron to try different values?

                
                


