# from pdb import set_trace as breakpoint
# from math import *
# import re
# import os, glob
# import sys
# import random
# from yices import *
# from collections import defaultdict
# from sympy import Symbol
# from sympy.logic.inference import satisfiable
# import numpy as np 

def cleanlines(line):
    line1 = line.replace('end','')
    if 'if(' in line or 'if ' in line:
        line2 = line1.replace('if ','')
        line2 = line2.replace('if(','')
    else:
        line2 = line1
    line3 = line2.replace('else','')
    line4 = line3.replace('begin','')
    line5 = line4.replace('\t','')
    line6 = line5.replace('\n','')
    line7 = line6.replace('\r','')
    if '//' in line7:
        line7 = line7.split('//')[0]
    return line7

def Model_check(module, lines):
    bug = 0
    Check = []
    if module == []:
        return bug

    #if "n27 activeroute <= {{CHANNELS-1{1'b0}},1'b1}; 1" in module:
    #    print(module)
    #    breakpoint()
    index1 = 0
    index2 = 0
    done = 0
    Trigger = 0
    while done != 1:
        # breakpoint()
        check1 = []
        check2 = []
        
        for x1 in lines:        
            if int(x1.split()[-1]) == index1:
                x1 = x1.split()
                x1.pop(-1)
                x1 = ' '.join(x1)
                check1.append(x1)
            else:
                continue
        #index1 = index1 + 1

        for x2 in module:
            x2 = x2.replace(';','')
            if int(x2.split()[-1]) == index2:
                x2 = x2.split()
                x2.pop(-1)
                x2 = ' '.join(x2)
                check2.append(x2)
            else:
                continue
        if check2 == []:
            done = 1
            continue
        index2 = index2 + 1
        if '==' in check1[0]:
            Trigger = 1
            if check1[0] in check2:
                index1 = index1 + 1
        elif '<=' in check1[0]:
            correct = 0
            for x in check1:
                xcheck = x.split('<=')
                for y in check2:
                    ycheck = y.split('<=')
                    if xcheck[0] == ycheck[0]:
                        if xcheck[1] == ycheck[1]:
                            correct = correct + 1
                            continue
                        else:
                            if Trigger == 1:
                                bug = 1
                                return bug
                        
                    else:
                        continue
            if Trigger == 1:
                if (correct == len(check1) or correct == 0):
                    continue
                elif correct < len(check1):
                    bug = 1
                    return bug
            elif Trigger == 0:
                if (correct == len(check1) or correct == 0):
                    continue
                elif correct < len(check1):
                    bug = 1
                    return bug
           
    return bug        
        
#--------------------------------------------------------------

specline = []
with open('spec.txt') as fl:
    lines = fl.readlines()
fl.close()
for line in lines:
    specline1 = []
    specline2 = []
    flow = 0
    line1 = line.split('/')
    #breakpoint()
    if len(line1) > 1:
        line1[1] = cleanlines(line1[1])
        line3 = line1[1].split(';')
        specline1.append(line1[0] + ' ' + str(flow))
        for linex in line3:
            line2 = linex.split('"')
            for index, linex1 in enumerate(line2):
                if linex1 == '':
                    continue
                specline1.append(linex1 + ' ' + str(flow))
                if index == 0:
                    flow = flow + 1
        specline2.append(', '.join(specline1) )
    else:
        line = cleanlines(line)
        line3 = line.split(';')
        for index2 ,linex in enumerate(line3):
            line2 = linex.split('"')
            flow = index2
            for index, linex1 in enumerate(line2):
                if linex1 == '':
                    continue
                specline1.append(linex1 + ' ' + str(flow))
                if index == 0 and '<=' in linex1:
                    continue
                elif index == 0:
                    flow = flow + 1
        specline2.append(', '.join(specline1) )
    specline.append(specline2)
print('Specline: \n', specline, '\n')
# breakpoint()

flpath = 'ram/'
file1 = 'file_list.txt'
specline = specline[0]
specline = specline[0]
specline = specline.split(',')
x = 1
number = 0
while x == 1:
    try: fl = open('Extracted_CFG_' + str(number) + '.txt')
    except: x = 0
    if x == 1:
        number = number + 1
        lines = fl.readlines()
        fl.close()
        checklines = []
        changed = 0
        for line in lines:
            if 'n0' in line:
                if changed == 1:
                    continue
            else:
                changed = 1
            line = line.replace('assign','')
            if '==' in line:
                line = line.split()
                line.pop(0)
                line = ' '.join(line)
                checklines.append(line)
            elif '<=' in line:
                line = line.split()
                line.pop(0)
                line = ' '.join(line)
                checklines.append(line)
            elif '=' in line:
                line = line.split('=')
                line = ' <= '.join(line)
                line = line.split()
                line.pop(0)
                line = ' '.join(line)
                checklines.append(line)
            elif 'always' in line:
                if 'True' in line:
                    continue
                else:
                    if changed == 0:
                        checklines.append(line + ' 0')
            else:
                modulename = line
        # breakpoint()
        
        bug = Model_check(checklines, specline)
        if bug == 1:
           
            print('Modulename: ', modulename, '\n')
            print('Checklines: ', checklines, '\n')
            
    else:
       continue

print('---------------------done with modules---------------------\n')




