#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Magnifico script de python para fazer coisas para a Ana.
Feito por José Antunes @ INESC-MN 2013
Dúvidas: jose.antunes@ist.utl.pt
"""


""" Imports for program """
import sys
import fnmatch
from os import listdir, name, system, getcwd
from os.path import isfile, join
from math import log

""" Hello function """
def Hello_World():
    system('cls' if name=='nt' else 'clear')
    print "____________________________________"
    print " ____      __  __ _               _ "
    print "|_  /___  |  \/  (_)__ _ _  _ ___| |"
    print " / // -_) | |\/| | / _` | || / -_) |"
    print "/___\___| |_|  |_|_\__, |\_,_\___|_|"
    print "                   |___/            "
    print "____________________________________"
    
""" Help function for argument errors """
def help(args):
    print "\n"
    print "Incorrect number of arguments. (Num of Args: %d - Expected: 1)" % (len(args)-1)
    print("Argument: %s" % args[1] if len(args) > 1 else "No arguments")
    print "Write fpm for Full Path Mode"
    print "or"
    print "Write idm for In Directory Mode"
    print "_______________________________"
    print "Example: \"python %s fpm\"" % args[0]
    print "\n"

""" Check operative system """    
def check_OS():
    # Check Operative System being used
    print "OS: %s " % name
    
    return name


""" Function to read files in directory """
def fpm(full_path):
    #/Users/jose/Documents/py_tests/Ana_Inesc/t899D6B6
    print full_path
    try:
        onlyfiles = [f for f in listdir(full_path) if isfile(join(full_path,f)) ]
        onlyfiles = fnmatch.filter(onlyfiles, '_*.DAT')
        if len(onlyfiles)==0: raise OSError
    except OSError:
        print "No directory or .dat files found"
        sys.exit()
         
    print "%d .dat files were found" % len(onlyfiles)
    print ""
    while True:
        option = raw_input("Find files based on V_bias or H field? ( V / H ): \n").lower()
        if option == "v" or option == "h":
            break
        else:
            print "%s is not valid. Choose V or H" % option
    
    if option == "v":
        v_bias(full_path, onlyfiles)
    elif option == "h":
        h_field(full_path, onlyfiles)
    else:
        print "Program Error"
        sys.exit()

""" Definition of h_field function """
def h_field(full_path, files):
    origin = "h_field"
    accepted_values = range(-15,6,1) + range(5,-16,-1)

    while True:
        valor = raw_input("H_field value applied in mT?: \n")
        try:
            if int(valor) in accepted_values:
                break 
        except ValueError: pass

        print "%s is not valid. Choose an int between -15 and 5" % valor
        print "in steps of 1 mT"

    indices = [indice for indice, x in enumerate(accepted_values) if x == int(valor)]
    
    final_filter_keys = []
    final_files = []
    
    for indice in indices:
        filter_keys = '_B10'
        if len(str(indice)) < 2:
            filter_keys = '*' + filter_keys + "0" + str(indice) + '.DAT'
        else:
            filter_keys = '*' + filter_keys + str(indice) + '.DAT'

        final_filter_keys.append(filter_keys)

    for key in final_filter_keys:
        final_files.append(fnmatch.filter(files, key)) 
        

    final_files = final_files[0] + final_files[1]
    print "%d .dat files were found" % len(final_files)
    print final_files
    use_files(full_path, final_files, origin, int(valor))
    

""" Definition of V_Bias function """
def v_bias(full_path, files):
    origin = "v_bias"
    accepted_values = [((-1)**(x-1))*(x*10) for x in range(58)]
    while True:
        valor = raw_input("V_bias value applied in mV?: \n")
        try:
            if int(valor) in accepted_values:
                break
        except ValueError: pass
        print "%s is not valid. Choose an int between 10, -20, ..., 570" % valor
        print "in steps of 10 mV"
    
    filter_keys = '_A10'
    
    if len(str(accepted_values.index(int(valor)))) < 2:
        filter_keys = filter_keys + "0" + str(accepted_values.index(int(valor))) + '*.DAT'
    else:
        filter_keys = filter_keys + str(accepted_values.index(int(valor))) + '*.DAT'
    
    
    print filter_keys
    files = fnmatch.filter(files, filter_keys)  
    print "%d .dat files were found" % len(files)

    use_files(full_path, files, origin,int(valor))
    
def use_files(full_path, files, origin, valor):
    from pprint import pprint
    import matplotlib.pyplot as pl
    import csv

    file_list = []
    for file_name in files:
        file_name = full_path + "/" + file_name
        file_list.append(file_name)
    
    if origin == "v_bias":
        print "Choose + for H field from -15 mT to 5 mT \n or \n Choose - for H field from 5 mT to -15 mT"
        while True:
            volta = raw_input()
            if volta == "+":
                file_list = file_list[:21]
                break
            elif volta == "-":
                file_list = file_list[21:]
                break
            else: print "Choose + or - ."
    if origin == "h_field":
        print ("Choose:\n\
        1) %d mT in -15mT to 5mT cycle\n\
        2) %d mT in 5mT to -15mT cycle") % (valor, valor)
        while True:
            volta = raw_input()
            if volta == "1":
                file_list = file_list[:57]
                break
            elif volta == "2":
                file_list = file_list[57:]
                break
            else: print "Choose 1 or 2 ."

    final_array = []

    pprint(file_list)
    for file_name in file_list:
        final_array = final_array + lerCSV(file_name, origin)

    file_name = ("Campo" if origin == "h_field" else "Dif_Potencial") \
    + str(valor) + ("mT" if origin == "h_field" else "mV") + ".csv"
    with open(file_name, "wb") as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for row in final_array:
            writer.writerow(row)
            
    #pl.plot(zip(*final_array)[0],zip(*final_array)[1],"b.")
    #pl.show()
    #pprint(final_array)


def lerCSV(path, origin):
    import matplotlib.pyplot as pl
    import csv

    frequency = []
    amplitude = []
    
    filereader = csv.reader(open(path,'rb'), delimiter='\t') #defines the reader
    for row in filereader:
        frequency.append(float(row[0]))
        amplitude.append(float(row[1]))


    if origin == "v_bias":
        B_file_number = int(path[-6:-4])
        field = range(-15,6,1) + range(5,-16,-1)
        field = field[B_file_number]
        constant = [field]*len(frequency)
    if origin == "h_field":
        A_file_number = int(path[-12:-10])
        voltage = ((-1)**(A_file_number-1))*(A_file_number*10)
        constant = [voltage]*len(frequency)
        
    #print "-------- ARRAYS FINAIS -------"
    
    assert len(frequency) == len(amplitude)
    dados3d = zip(constant, frequency, amplitude)
    
    
    # for x in graphtv:
    #     print "frequency %.3f - amplitude: %.3f" % (x[0],x[1])
    return dados3d

    

""" Definition of main function """   
if __name__ == "__main__":
    Hello_World()
    check_OS()
    
    if len(sys.argv) != 2:
        help(sys.argv)
        sys.exit()
    
    arg1 = sys.argv[1].lower()
    
    if arg1 == 'fpm':
        fpm(raw_input("Full path to directory: "))
    elif arg1 == 'idm':
        fpm(getcwd())
    else:
        help(sys.argv)
        sys.exit()
    
    