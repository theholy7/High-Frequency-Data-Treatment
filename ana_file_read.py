#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as pl

def lerCSV(path):
    frequency = []
    amplitude = []
    
    filereader = csv.reader(open(path,'rb'), delimiter='	') #defines the reader
    for row in filereader:
        frequency.append(float(row[0]))
        amplitude.append(float(row[1]))
        
    print "-------- ARRAYS FINAIS -------"
    
    assert len(frequency) == len(amplitude)
    graphtv = zip(frequency, amplitude)
    
    for x in graphtv:
        print "frequency %.3f - amplitude: %.3f" % (x[0],x[1])
        
    pl.plot(frequency,amplitude,"b.")
    #pl.axis([0, 23000, 0, 0.002])
    pl.show()
    return graphtv
    
path = 't899D6B6/_A1000_B1035.dat'
a = lerCSV(path)
