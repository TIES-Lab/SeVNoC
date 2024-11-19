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

def Nodeflow_reset(Nodeflow):
    #breakpoint()
    rst_sign = 0
    Nodeinfo = []
    modulename = ''
    Trigger = []
    with open('spec.txt') as fl:
        lines = fl.readlines()
    fl.close()
    for line in lines:
        line1 = line.split('/')
        #breakpoint()
        if len(line1) > 1:           
            if ';' in line1[1]:
                line3 = line1[1].split(';')
                for lines3 in line3:
                    line2 = lines3.split('"')
                    for line4 in line2:
                        Trigger.append(line4.split()[0]) 
            else:
                line2 = line1[1].split('"')
                for line4 in line2:
                    Trigger.append(line4.split()[0])     
        else:
            if ';' in line:
                line3 = line.split(';')
                for lines3 in line3:
                    line2 = lines3.split('"')
                    for line4 in line2:
                        Trigger.append(line4.split()[0])      
            else:
                line2 = line.split('"')
                for line4 in line2:
                    Trigger.append(line4.split()[0])   
    #breakpoint()
    nodetoreach = []
    for item in Nodeflow:
        #if 'data_last_buf' in item:
        #    print(item)
        #    breakpoint()
        if isinstance(item, str):
            modulename = item
            continue
        #breakpoint()
        for index, items in enumerate(item):
            #breakpoint()
            if 'always' in items:
                #breakpoint()
                if rst_sign == 0 and Nodeinfo != []:
                    Nodeinfo.pop(len(Nodeinfo)-1)
                    Nodeinfo.append(item)
                    rst_sign = 0
                elif rst_sign == 1:
                    Nodeinfo.append(item)
                    rst_sign = 0
                elif rst_sign == 0:
                    #Nodeinfo.pop(len(Nodeinfo)-1) 
                    Nodeinfo.append(item)
                    rst_sign = 0
            elif 'always' not in items:
                #breakpoint()
                #if ('rst' in items or 'reset' in items) and 'or' not in items and 'and' not in items and index == 0 and 'burst' not in items:
                #    newitem = []
                #    for instances in item:
                #        if isinstance(instances, str):
                #            newitem.append(instances)
                #    Nodeinfo.append(newitem)
                #    rst_sign = 1
                #    continue
                for signal in Trigger:
                    try: x = items.split()[1]
                    except: break
                    if (x == signal and '==' in items) or (x == signal and '<=' in items):
                        nodetoreach.append(items.split()[0])
                        #breakpoint()
                        newitem = []
                        for instances in item:
                            if isinstance(instances, str):
                                newitem.append(instances)
                        if newitem in Nodeinfo:
                            continue
                        Nodeinfo.append(newitem)
                        #breakpoint()
                        if Nodeinfo[0] != modulename:
                            Nodeinfo.insert( 0, modulename)
                        rst_sign = 1
                        break
    #breakpoint()      
    Nodeinfox = []
    #for x in nodetoreach:
    #    checkdone = 0
    #    predecessors4 = []
        #breakpoint()
    #    Nodeflow.pop(0)
    #    flowx = Nodeflow
    #    checkdone = EdgeRealignment(flowx, predecessors4, x)
        #path.append(predecessors4)
        #breakpoint()
    #    if checkdone == -1:
    #        continue
    #    elif checkdone == 2 or checkdone == 0:
    #        print(predecessors4) 
    #        Nodeinfox.append(predecessors4)
    #breakpoint()
    #Nodeinfo.insert( 0, modulename)
    if Nodeinfo == []:
        return Nodeinfo
    elif len(Nodeinfo[len(Nodeinfo)-1]) == 1 and 'always' in Nodeinfo[len(Nodeinfo)-1][0]:
         Nodeinfo.pop(len(Nodeinfo)-1)
    #if Nodeinfo != []:
    #     Nodeinfo.pop(0)
    #breakpoint()
    return Nodeinfo


def clockedge(lines, index4, node, Nodeinfo, case):
     always = []
     always1 = []
     linelist = list(lines[index4])
     begin = 1
     print(lines[index4])
     #breakpoint()
     line = lines[index4].replace('always','').replace('_ff','').replace('_comb','')
     if ':' in line:
         line = line.split(':')[0]
     line1 = line.replace('(','')
     line2 = line1.replace(')','')
     line3 = line2.replace('@','')  
     line4 = cleanlines(line3)
     i = 0
     if ',' in line4:
         line5 = line4.split(',')
         for i in range(len(line5)):
             if 'posedge' in line5[i]:
                 line6 = line5[i].split()
                 always.append(line6[1] + " == 1")
             elif 'negedge' in line5[i]:
                 line6 = line5[i].split()
                 always.append(line6[1] + " == 0")
         always1.append('always ' + ' or '.join(always))
         Nodeinfo.append(always1)
     elif 'or' in line4:
         line5 = line4.split('or')     
         for i in range(len(line5)):
             if 'posedge' in line5[i]:
                 line6 = line5[i].split()
                 always.append(line6[1] + " == 1")
             elif 'negedge' in line5[i]:
                 line6 = line5[i].split()
                 always.append(line6[1] + " == 0")
         always1.append('always ' + ' or '.join(always))
         Nodeinfo.append(always1)
     elif '*' in line4:
         always.append('always ' + "True")
         Nodeinfo.append(always)
     else:
         line5 = line4
         if 'posedge' in line5:
             line6 = line5.replace('posedge','')
             always.append('always ' + line6 + " == 1")
         elif 'negedge' in line5:
             line6 = line5.replace('negedge','')
             always.append('always ' + line6 + " == 0")
         Nodeinfo.append(always)
     a = 1
     assignment = []
     linelist = list(lines[index4])
     indentcount = 0
     if 'begin' not in lines[index4] or 'always' in lines[index4]:
         for indent in linelist:
             if indent == '\t':
                 indentcount = indentcount + 8
             elif indent == ' ':
                 indentcount = indentcount + 1
             elif indent != ' ':
                 break
     indentcount1 = indentcount + 1
     #if 'always_comb' in lines[index4]:
     ##    print(lines[index4])
     #    breakpoint()
         
     while begin != 0 and indentcount1 > indentcount:
         #breakpoint()
         
         line = lines[index4 + a] 
         if 'begin' == line.split() and 'always' in lines[index4 + a - 1]:
             begin = begin - 1
         if '//' in line:
             nextline = line.split('//')
             line = nextline[0].replace('\n','')
         if line == '':
             a = a + 1
             continue
         if  'begin' in line:
             begin = begin + 1
         if 'end' in line:
             begin = begin - 1
         else:
             begin = begin
         if begin == 1:
             print(line + 'begin: ' + str(begin))   
             if '=' in line and ('if ' not in line and 'if(' not in line):    
                 if 'assign' in line:
                     line1 = line.replace('assign','')
                     line2 = line1.split()
                     line3 = ' '.join(line2)
                     if '<=' in line3:
                         line3 = line3.replace('<=',' <= ')
                     elif '=' in line3:
                         line3 = line3.replace('=',' <= ')
                     assignment.append('n0 ' + line3 + ' 0')
                 else:
                     line2 = line.split()
                     line3 = ' '.join(line2)
                     if '<=' in line3:
                         line3 = line3.replace('<=',' <= ')
                     elif '=' in line3:
                         line3 = line3.replace('=',' <= ')
                     assignment.append('n0 ' + line3 + ' 0')
             else:
                 a = a + 1
                 continue
             a = a + 1
         elif begin > 1:
             
             a = a + 1
         if lines[index4 + a] != '':
             linelist = list(lines[index4 + a])
             indentcount1 = 0
             for indent in linelist:
                 if indent == '\t':
                     indentcount1 = indentcount1 + 8
                 elif indent == ' ':
                     indentcount1 = indentcount1 + 1
                 elif indent != ' ':
                     break
         if begin == 0:
             print(lines[index4 + a] + 'begin: ' + str(begin))
     else:
         
         if assignment != []:
             Nodeinfo.append(assignment)
     #breakpoint()
     return Nodeinfo, index4 + i , node
     

def ifelsecondition(lines, index4, node, Nodeinfo, case):
    ifcond = 1
    oneline = 0
    Connection = 0
    #if 'data_last_buf' in lines:
    #    print(lines[index4])
    #    breakpoint()
        
    linelist = list(lines[index4])
    print(lines[index4])
    #breakpoint()
    line = lines[index4]
    if case == 1:
        #breakpoint()
        line = []
        count = 0
        for index, val in enumerate(linelist):
            if ':' in val and count == 0:
                line = []
                count = 1
                continue
            line.append(val)
        line = ''.join(line)
    indentcount = 0
    #breakpoint()
    
    values = line.split()
    for indent in linelist:
        if indent == '\t':
            indentcount = indentcount + 8
        elif indent == ' ':
            indentcount = indentcount + 1
        elif indent != ' ':
            break
    for vals in values:
        if vals == '=' or vals == '<=':
            oneline = 1
    if oneline == 1:
        values, valueline = onelinecondition(values)
        line = ' '.join(values)
    Condition = []  
    #breakpoint()                 
    #if '&&' in y1 and Condition == []:
    line7 = cleanlines(line)
    line8 = line7.split()
    if '&&' in values or '||' in values or '&' in values:
        #breakpoint()
        Condition1 = []
        if '&&' in line7:
            line10 = line7.split('&&')#.split('||')
        if '&' in line7:
            line10 = line7.split('&')
        else:
            line10 = line7
        for ii, instance1 in enumerate(line10):
            if '||' in instance1:
                instance2 = instance1.split('||')
                line10.pop(ii)
                for newitem in instance2:
                    line10.insert(ii, newitem)
        #breakpoint()
        for instance in line10:
            if '==' in instance or '>=' in instance:
                instance = instance.replace(' ','').replace('(','').replace(')','')
                continue
            elif '!=' in instance:
                instance = instance.replace(' ','').replace('(','').replace(')','')
                continue
            elif '~' in instance or '!' in instance and '!=' not in instance:
                instance = instance.replace(' ','').replace('(','').replace(')','')
                Condition1.append(instance.replace('~','').replace('!','') + ' == 0 ')
            else:
                instance = instance.replace(' ','').replace('(','').replace(')','')
                Condition1.append(instance + ' == 1 ')
        for index1, elements in enumerate(line8):
            if '&&' == elements or '||' == elements:
                continue
            if '==' in elements:
                continue
            for replacement in Condition1:
                if elements.replace('~','').replace('!','').replace('(','').replace(')','') in replacement:
                    line8[index1] = line8[index1].replace(elements, replacement)
                elif elements.replace(' ','').replace('(','').replace(')','') in replacement:
                    line8[index1] = line8[index1].replace(elements, replacement)
        line8 = " ".join(line8).replace('(','').replace(')','')
        line9 = line8.replace('&&',' and ')
        line10 = line9.replace('||',' or ')
        line10 = line10.replace('&', ' and ')
        Condition.append('n' + str(node) + ' ' + line10 + " "+ str(Connection))
        node = node + 1
        Connection = Connection + 1
        nextline = lines[index4 + 1]
    else:
        #breakpoint()
        line10 = line7.replace('(','').replace(')','')
        line10 = line10.replace(' ','')
        if '==' in line10 or '>=' in line10:
            line8 = line10.replace('==',' == ').replace('>=',' >= ')
        elif '!=' in line10:
            line8 = line10.replace('!=',' != ')
        elif '~' in line10 or '!' in line10 and '!=' not in line10:
            line8 = line10.replace('~','').replace('!','') + ' == 0 '
        else:
            line8 = line10 + ' == 1 '
        
        Condition.append('n' + str(node) + ' ' + line8 + " "+ str(Connection))
        nextline = lines[index4 + 1]
        node = node + 1
        Connection = Connection + 1

    if oneline == 1:
        Condition.append('n' + str(node) + ' ' + valueline + " "+ str(Connection))
        node = node + 1
    if 'rst' in lines[index4]:
        #breakpoint()
        print(lines[index4])
    i = 1
    stop = 0
    checkb = 0
    while stop != 1:
        oneline = 0
        #if "activeroute <= {{CHANNELS-1{1'b0}},1'b1};" in nextline:
        #    breakpoint()
        #    print(nextline)
        try: nextnextline = lines[index4+1+i]
        except: nextnextline = ''
        if ('end' in nextline or ':' in nextline) and 'else' not in nextnextline and 'else' not in nextline:
            #breakpoint()
            indent2 = 0
            nextlinelist = list(nextline)
            for value in nextlinelist:
                if value == '\t':
                    indent2 = indent2 + 8
                elif value == ' ':
                    indent2 = indent2 + 1
                elif value != ' ':
                    break
            if indent2 <= indentcount:
                #Nodeinfo.append(Condition)
                stop = 1
        if 'case' in nextline and 'endcase' not in nextline and '//' not in nextline and ('case(' in nextline or 'case (' in nextline):
            nextlinecheck = lines[index4 + i]
            x = i
            while  'endcase' not in nextlinecheck:#':' not in nextlinecheck and
                x = x + 1
                nextlinecheck = lines[index4 + x]
            Nodeinfo1 = []
            Nodeinfo1, index3, node = casestatement(lines, index4 + i, node, Nodeinfo1, ifcond)
            for nodeflow in Nodeinfo1:
                if isinstance(nodeflow, str):
                    Condition.append(nodeflow)
            i = x
            nextline = lines[index4 + i]
            continue
        elif 'always' in nextline:
            indent2 = 0
            nextlinelist = list(nextline)
            for value in nextlinelist:
                if value == '\t':
                    indent2 = indent2 + 8
                elif value == ' ':
                    indent2 = indent2 + 1
                elif value != ' ':
                    break
            if indent2 <= indentcount:
                #Nodeinfo.append(Condition)
                stop = 1
                continue
            Nodeinfo1 = []
            #breakpoint()
            Nodeinfo1, index3, node = clockedge(lines, index4+i, node, Nodeinfo1, case)            
            i = index3 - index4 + 1
            #breakpoint()
            for nodeflow in Nodeinfo1:
                for nodeflows in nodeflow: 
                    if Condition == []:
                        nodeflows1 = (nodeflow + ' 0').replace('always', 'n'+ node)
                        node = node + 1
                        nodeflows1 = ' '.join(nodeflows1.split())
                        Condition.append(nodeflows1)
                        
                    elif Condition != []:
                        thisflow = int(Condition[len(Condition)-1].split()[len(Condition[len(Condition)-1].split())-1])
                        #nodeflows = Nodeinfo.pop()
                        newflow =  thisflow
                        nodeflows1 = (nodeflows + ' ' + str(newflow)).replace('always', 'n'+ str(node))
                        node = node + 1
                        nodeflows1 = ' '.join(nodeflows1.split())
                        Condition.append(nodeflows1)
            nextline = lines[index4 + i]
            #breakpoint()
        elif ('if ' in nextline or 'if(' in nextline) and 'else' not in nextline and (('if(' in nextline and ')' in nextline) or ('begin' in lines[index4 + i] or 'begin' in lines[index4 + i + 1])) :
            #breakpoint()
            indent1 = 0
            nextlinelist = list(nextline)
            for value in nextlinelist:
                if value == '\t':
                    indent1 = indent1 + 8
                elif value == ' ':
                    indent1 = indent1 + 1
                elif value != ' ':
                    break
            if indent1 <= indentcount:
                stop = 1
                #index4 = index4 + i
            elif indentcount < indent1:
                Nodeinfo1 = []
                #breakpoint()
                #if 'data_last_buf' in lines[index4+i+1]:
                #    print(nextline)
                #    breakpoint()
                Nodeinfo1, index3, node = ifelsecondition(lines, index4 + i, node, Nodeinfo1, case)
                i = index3 - index4
                
                if Condition == []:
                    for nodeflow in Nodeinfo1:
                        for nodeflows in nodeflow: 
                        #if Condition == []:
                            nodeflows1 = nodeflows.replace(nodeflows[len(nodeflows)-1], '0')
                            node = node + 1
                            #nodeflows1 = ' '.join(nodeflows1.split())
                            Condition.append(nodeflows1)
                        
                elif Condition != []:
                    thisflow = int(Condition[len(Condition)-1].split()[len(Condition[len(Condition)-1].split())-1])
                    for nodeflow in Nodeinfo1:
                        for nodeflows in nodeflow: 
                            if isinstance(nodeflows ,str):
                                #thisflow = int(Condition[len(Condition)-1].split()[len(Condition[len(Condition)-1].split())-1])
                                #nodeflows = Nodeinfo.pop()
                                newflow =  thisflow + int(nodeflows.split()[len(nodeflows.split())-1])
                                nodeflows1 = nodeflows.replace(nodeflows[len(nodeflows)-1], str(newflow))
                                #node = node + 1
                                nodeflows1 = ' '.join(nodeflows1.split())
                                Condition.append(nodeflows1)
                            else:
                                Condition = nodeflowadd(Condition, nodeflows, thisflow)
               # for nodeflow in Nodeinfo1:
               #     for nodeflows in nodeflow:
               #         newflow = int(nodeflows[len(nodeflows)-1]) + thisflow
               #         nodeflows1 = nodeflows.replace(nodeflows[len(nodeflows)-1], str(newflow))
               #         Condition.append(nodeflows1)
                nextline = lines[index4 + i]
        elif 'else if' in nextline:
            print(nextline)
            #breakpoint()
            #Nodeinfo.append(Condition)
            values = nextline.split()
            for vals in values:
                if vals == '=' or vals == '<=':
                    oneline = 1
            if oneline == 1:
                values, valueline = onelinecondition(values)
                line = ' '.join(values)
            #Condition = []                   
            line7 = cleanlines(nextline)
            line8 = line7.split()
            if '&&' in values or '||' in values or '&' in values:
                Condition1 = []
                if '&&' in line7:
                    line10 = line7.split('&&')#.split('||')
                if '&' in line7:
                    line10 = line7.split('&')
                for ii, instance1 in enumerate(line10):
                    if '||' in instance1:
                        instance2 = instance1.split('||')
                        line10.pop(ii)
                        for newitem in instance2:
                            line10.insert(ii, newitem)
                for instance in line10:
                    if '==' in instance or '>=' in instance:
                        instance = instance.replace(' ','').replace('(','').replace(')','')
                        continue
                    elif '~' in instance or '!' in instance:
                        instance = instance.replace(' ','').replace('(','').replace(')','')
                        Condition1.append(instance.replace('~','').replace('!','') + ' == 0 ')
                    else:
                        instance = instance.replace(' ','').replace('(','').replace(')','')
                        Condition1.append(instance + ' == 1 ')
                for index1, elements in enumerate(line8):
                    if '&&' == elements or '||' == elements:
                        continue
                    if '==' in elements:
                        continue
                    for replacement in Condition1:
                        if elements.replace('~','').replace('!','').replace('(','').replace(')','') in replacement:
                            line8[index1] = line8[index1].replace(elements, replacement)
                #breakpoint()
                line8 = " ".join(line8).replace('(','').replace(')','')
                line9 = line8.replace('&&',' and ')
                line10 = line9.replace('||',' or ')
                line10 = line10.replace('&',' and ')
                Condition.append('n' + str(node) + ' ' + line10 + " "+ str(Connection))
                node = node + 1
                Connection = Connection + 1
                i = i + 1
                nextline = lines[index4 + i]
            else:
                line10 = line7.replace('(','').replace(')','')
                line10 = line10.replace(' ','')
                if '==' in line10 or '>=' in line10:
                    line8 = line10
                elif '~' in line10:
                    line8 = line10.replace('~','') + ' == 0 '
                else:
                    line8 = line10 + ' == 1 '
        
                Condition.append('n' + str(node) + ' ' + line8 + " "+ str(Connection))
                i = i + 1
                nextline = lines[index4 + i]
                node = node + 1
                Connection = Connection + 1
            if oneline == 1:
                Condition.append('n' + str(node) + ' ' + valueline + " "+ str(Connection))
                node = node + 1

        elif 'else' in nextline and 'if' not in nextline:
            #breakpoint()
            #Nodeinfo.append(Condition)
            i = i + 1
            values = nextline.split()
            for vals in values:
                if vals == '=' or vals == '<=':
                    oneline = 1
            if oneline == 1:
                values, valueline = onelinecondition(values)
                line = ' '.join(values)
            #Condition = []
            Connection = Connection + 1
            nextline = lines[index4 + i]
            if oneline == 1:
                Condition.append('n' + str(node) + ' ' + valueline + " "+ str(Connection))
                node = node + 1
            
        elif '<=' in nextline or '=' in nextline:
            #breakpoint()
            #if 'data_last_buf' in nextline:
            #    print(nextline)
            #    breakpoint()
            nextline9 = cleanlines(nextline)
            nextline9 = nextline9.replace(' ','')#cleanup
            if '{' in nextline9 and '}' not in nextline9:
                #breakpoint()
                i = i + 1
                nextline = lines[index4 + i]
                continue
                if '<=' in nextline9:
                    Condition2 = 'n' + str(node) + " " + nextline9.replace('<=',' <= ').replace('`','').replace(';','')
                elif '=' in nextline9:
                    Condition2 = 'n' + str(node) + " " + nextline9.replace('=',' <= ').replace('`','').replace(';','')
                checkb = 1
                node = node + 1
                continue

            nextline9 = nextline9.replace('<=',' <= ')
            Condition.append('n' + str(node) + " " + nextline9 + ' ' + str(Connection))
            node = node + 1
           # values = nextline.split()
           # for index, y in enumerate(values):
           #     if '<=' in y:
           #         if values[index - 1] not in State:
           #             State.append(values[index - 1])
            
            i = i + 1
            nextline = lines[index4 + i]
        elif checkb == 1:
            nextline3 = nextline.replace(' ','').replace('\n','').replace('\t','')
            Condition2 = Condition2 + " " + nextline3 
            if '}' in nextline:
                checkb = 0
                Condition2 = Condition2 + ' ' + str(Connection)
                Condition.append(Condition2)
        else:
            if cleanlines(nextline) == '' or 'else' in nextnextline :
                i = i + 1
                nextline = lines[index4 + i]
                continue
            if cleanlines(line) != '':    
                indent2 = 0
                nextlinelist = list(nextline)
                for value in nextlinelist:
                    if value == '\t':
                        indent2 = indent2 + 8
                    elif value == ' ':
                        indent2 = indent2 + 1
                    elif value != ' ':
                        break
                if indent2 <= indentcount:
                #Nodeinfo.append(Condition)
                    stop = 1
                    continue
                else:
                    i = i + 1
                    nextline = lines[index4 + i]
            else:
                i = i + 1
                nextline = lines[index4 + i]
    else:
        #breakpoint()
        if Condition != []:
            Nodeinfo.append(Condition)
        return Nodeinfo, index4 + i , node

def nodeflowadd(Condition, nodeflows, thisflow):
    for nodeflows1 in nodeflows: 
        if isinstance(nodeflows ,str):
            newflow =  thisflow + int(nodeflows.split()[len(nodeflows.split())-1])
            nodeflows1 = nodeflows.replace(nodeflows[len(nodeflows)-1], str(newflow))
            nodeflows1 = ' '.join(nodeflows1.split())
            Condition.append(nodeflows1)
        else:
            Condition = nodeflowadd(Condition, nodeflows1, thisflow)
    return Condition
   
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

def onelinecondition(values):
    x = []
    x1 = []
    #breakpoint()
    for index, val in enumerate(values):
        if ':' in val and 'if' not in values:
            x = []
            continue
        x.append(val)
        if val == '<=' or val == '=':
            x.pop()
            x.pop()
            break
    for index1, val in enumerate(values):
        if index1 < index - 1:
            continue
        x1.append(val)
    #breakpoint()
    x1 = ' '.join(x1)
    if '<=' in x1:
        x1 = x1.replace('<=',' <= ').replace('`','').replace(';','') 
    elif '=' in x1 and '==' not in x1:
        x1 = x1.replace('=',' <= ').replace('`','').replace(';','')
    return x, x1

def casestatement(lines, index4, node, Nodeinfo, ifcond):
    case = 1
    print(lines[index4])
    line = lines[index4]
    linevalue = line.split('(')
    variable = linevalue[1].replace(')','').replace('\n','')
    i = 1
    nextline = lines[index4 + i]
    indentcount = 0
    values = line.split()
    linelist = list(lines[index4])
    for indent in linelist:
        if indent == ' ':
            indentcount = indentcount + 1
        elif indent != ' ':
            break
    Condition = []
    Connection = 0
    default = 0
    read = 0
    checkb = 0
    while 'endcase' not in nextline:
        #if (index4+i)>=324:
        #    nextline = 'endcase'
        #    continue
        #breakpoint()
        nextline = nextline.replace('\n','')
        if nextline.replace(' ','').replace('\t','').replace('\n','') == 'end':
            i = i + 1
            nextline = lines[index4 + i]
            continue
        nextline1 = nextline.split()
        nextline = ' '.join(nextline1)
        if '//' in nextline:
            nextline2 = nextline.split('//')
            nextline = nextline2[0].replace('\n','')
                                
            if 'end' in nextline:
                nextline = nextline.replace(' ','')
                if nextline == 'end':
                    i = i + 1
                    nextline = lines[index4 + i]
                    continue
        if nextline == '':
            i = i + 1
            nextline = lines[index4 + i]
            continue
        indent1 = 0
        variable1 = []
        #breakpoint()
        nextlinevalue = list(nextline)
        if 'default' in nextline:
            default = 1
            Nodeinfo.append(Condition)
            Condition = []
            assignment = nextline.split(':')
            assignment1 = assignment[1].split()
            #breakpoint()
            nextline3 = ' '.join(assignment1)
            if nextline3.replace(' ','') == 'begin' or nextline3.replace(' ','') == '':
                read = 1
                i = i + 1
                nextline = lines[index4 + i]
                continue
            if "'0" in nextline3 or "'1" in nextline3:
                nextline3 = nextline3.replace("'",'')
            if '<=' in nextline3:
                Condition.append('n' + str(node) + " " + nextline3.replace('<=',' <= ').replace('`','').replace(';','') + " " + str(Connection))
            elif '=' in nextline3:
                Condition.append('n' + str(node) + " " + nextline3.replace('=',' <= ').replace('`','').replace(';','') + " " + str(Connection))
               
                Nodeinfo.append(Condition)
                node = node + 1
                i = i + 1
                nextline = lines[index4 + i]
                continue
        elif 'if' in nextline and 'else' not in nextline and ':' not in nextline:
            #breakpoint()
            nextlinecheck = lines[index4 + i]
            x = i
            while ':' not in nextlinecheck and 'endcase' not in nextlinecheck:
                x = x + 1
                nextlinecheck = lines[index4 + x]
            #breakpoint()
                
            Nodeinfo1 = []
            Nodeinfo1, index3, node = ifelsecondition(lines, index4 + i, node, Nodeinfo1, case)
            
            
            for nodeflow in Nodeinfo1:
                if isinstance(nodeflow, str):
                    Condition.append(nodeflow)
            i = x
            nextline = lines[index4 + i]
            continue
        elif ':' in nextline and ('<='  in nextline or '=' in nextline or 'if' in nextline or 'begin' in nextline):
            #breakpoint()
            if Condition != []:
                Nodeinfo.append(Condition)
            Condition = []
            if nextline.count(':') > 1:
                assignment1 = nextline.split(':')
                assignment1.pop(0)
                assignment2 = ':'.join(assignment1)
                assignment = ['',assignment2]
            else:
                assignment = nextline.split(':')
        elif '<=' in nextline or '=' in nextline:
            assignment = nextline.split()
            nextline3 = ' '.join(assignment)
            if '<=' in nextline3:
                Condition.append('n' + str(node) + " " + nextline3.replace('<=',' <= ').replace('`','').replace(';','') + " " + str(Connection))
            elif '=' in nextline3:
                nextline3 = nextline3.replace('=',' <= ').replace('`','').replace(';','')
                if ' <=  <= ' in nextline3:
                    nextline3 = nextline3.replace(' <=  <= ', ' == ')
                Condition.append('n' + str(node) + " " + nextline3 + " " + str(Connection))
                                
            node = node + 1
        elif checkb == 1:
            nextline3 = nextline.replace(' ','').replace('\n','').replace('\t','')
            Condition2 = Condition2 + " " + nextline3 
            if '}' in nextline:
                checkb = 0
                Condition2 = Condition2 + ' ' + str(Connection)
                Condition.append(Condition2)
        for val in nextlinevalue:
            if val == ' ':
                indent1 = indent1 + 1
            else:
                variable1.append(val)
            
                equal = ''.join(variable1)
            if val ==':' and ('`' in nextline or "'h" in equal or "'b" in equal):
                #assignment
                #equal = ''.join(variable1)
                equal = equal.replace(':','')
                nextline3 =  variable + ' == ' + equal
                Condition.append('n' + str(node) + " " + nextline3.replace('`','').replace(';','') + " " + str(Connection))
                Connection = Connection + 1
                node = node + 1
                if len(nextline.split()) < 2:
                    break
                elif assignment[1] == '' or assignment[1].replace(' ','') == 'begin':
                    break
                elif 'if' in assignment[1]:
                    #breakpoint()
                    #nextline = assignment[1]
                    nextlinecheck = lines[index4 + i]
                    x = i
                    while (':' not in nextlinecheck or ('`' not in nextlinecheck and "'h" not in nextlinecheck and "'b" not in nextlinecheck )) and 'endcase' not in nextlinecheck:
                        x = x + 1
                        nextlinecheck = lines[index4 + x]
            #breakpoint()
                    
                    Nodeinfo1 = []
                    Nodeinfo1, index3, node = ifelsecondition(lines, index4 + i, node, Nodeinfo1, case)
                    

                    for nodeflow in Nodeinfo1:
                        if isinstance(nodeflow, str):
                            Condition.append(nodeflow)
                    
                    i = x
                    nextline = lines[index4 + i]
                    break
                    #break
                else:
                    assignment1 = assignment[1].split()
                    assignment1 = ' '.join(assignment1)
                    nextline3 = assignment1.replace(';','')
                    if ("'0" in nextline3 or "'1" in nextline3) and ':' not in nextline3:
                        nextline3 = nextline3.replace("'",'')
                        #breakpoint()
                        if '<=' in nextline3:
                            Condition.append('n' + str(node) + " " + nextline3.replace('<=',' <= ').replace('`','').replace(';','') + " " + str(Connection))
                        elif '=' in nextline3:
                            Condition.append('n' + str(node) + " " + nextline3.replace('=',' <= ').replace('`','').replace(';','') + " " + str(Connection))
                        node = node + 1
                        break
                    elif '{' in nextline3 and '}' not in nextline3:
                        if '<=' in nextline3:
                            Condition2 = 'n' + str(node) + " " + nextline3.replace('<=',' <= ').replace('`','').replace(';','')
                        elif '=' in nextline3:
                            Condition2 = 'n' + str(node) + " " + nextline3.replace('=',' <= ').replace('`','').replace(';','')
                        checkb = 1
                        node = node + 1
                        break
                    else:
                        if '<=' in nextline3:
                            Condition.append('n' + str(node) + " " + nextline3.replace('<=',' <= ').replace('`','').replace(';','') + " " + str(Connection))
                        elif '=' in nextline3:
                            #breakpoint()
                            nextline3 = nextline3.replace('=',' <= ').replace('`','').replace(';','')
                            if ' <=  <= ' in nextline3:
                                nextline3 = nextline3.replace(' <=  <= ', ' == ')
                            Condition.append('n' + str(node) + " " + nextline3 + " " + str(Connection))
                            
                        node = node + 1
                        break
        i = i + 1
        nextline = lines[index4 + i]
    else:
        if default == 0 or (default == 1 and read == 1):
            Nodeinfo.append(Condition)
        Condition = [] 
        return Nodeinfo, index4+i, node


def RealiCFG(flpath,file1):
    Module = []
    Condition = []
    Nodeinfo = []
    State = []
    i = 0
    node = 0
    ifcond = 0
    case = 0
    modulelist2 = []
    parameter = []
    #flpath = 'Advanced_Debugger_rtl/'
    with open(flpath + file1) as fl:
        #breakpoint()
        for block in fl:
            #breakpoint()
            if '.v' in block or '.sv' in block:
                Connection = 0
                with open(flpath + block.replace('\n','')) as fl1: 
                    lines = fl1.readlines()
                    fl1.close()
                    AlwaysValue = []
                formark = 0
                indentref = 0
                indent = 0
                indentmark = 0
                check = 0
                for index4,line in enumerate(lines):
                    #if 'FULLPACKET' in line:
                    #    print(block)
                    #    breakpoint()
                    if 'generate' in line.split():
                        nextlinelist = list(line)
                        for value in nextlinelist:
                            if value == '\t':
                                indent = indent + 8
                            elif value == ' ':
                                indent = indent + 1
                            elif value != ' ':
                                break
                        if indent<=indentref:
                            indentmark = 0
                            indent = 0
                            indentref = 0
                        else:
                            indent = 0
                    if 'module' in line and 'endmodule' not in line and 'module' == line.split()[0]:
                        #modulelist2 = []
                        check = 1
                        themodule = line.split()[1]
                        themodule1 = themodule.split('(')[0]
                        modulelist2.append(themodule1 + ' ')
                        print(modulelist2)
                        #breakpoint()
                        continue
                    if 'parameter' in line and '=' in line:
                        line = line.replace('parameter', '')
                        #if len(line) > 2:
                            #print(block)
                            #breakpoint()
                        line1 = line.split()
                        if len(line1) > 2:
                            for ind, things in enumerate(line1):
                                if '=' in line1[ind - 1]:
                                    things = things.replace(';','')
                                    para = para + ' ' + things
                                    break
                                elif '=' in line1[ind + 1]:
                                    para = things
                            
                            parameter.append(para)
                    if 'endmodule' in line:
                        parameter = []
                        check = 0
                        print(modulelist2)
                        #breakpoint()
                        for items in Nodeinfo:
                            modulelist2.append(items)
                        #moduleconnection.append(modulelist2)
                        continue
                    if check == 0:
                        continue
                    if 'always' in line:
                        #if 'always_comb' in line:
                        #    print(line + ' ' + block)
                        #    breakpoint()
                        Nodeinfo, index3, node = clockedge(lines, index4, node, Nodeinfo, case)
                    if 'if ' in line and ('begin' in line or 'begin' in lines[index4+1]) and 'else' not in line:
                        #breakpoint()
                        indent = 0
                        if indentmark == 0:
                            nextlinelist = list(line)
                            indent = 0
                            for value in nextlinelist:
                                if value == '\t':
                                    indent = indent + 8
                                elif value == ' ':
                                    indent = indent + 1
                                elif value != ' ':
                                    break
                            indentmark = 1
                            indentref = indent
                            indent  = 0
                        if indentmark == 1:
                            nextlinelist = list(line)
                            for value in nextlinelist:
                                if value == '\t':
                                    indent = indent + 8
                                elif value == ' ':
                                    indent = indent + 1
                                elif value != ' ':
                                    break
                            if indent<=indentref:
                                Nodeinfo, index3, node = ifelsecondition(lines, index4, node, Nodeinfo, case)
                                indent = 0
                            else:
                                indent = 0
                        
                    elif 'if ' in line or ('if(' in line and ')' in line):
                        #breakpoint()
                        indent = 0
                        if indentmark == 0:
                            nextlinelist = list(line)
                            for value in nextlinelist:
                                if value == '\t':
                                    indent = indent + 8
                                elif value == ' ':
                                    indent = indent + 1
                                elif value != ' ':
                                    break
                            indentmark = 1
                            indentref = indent
                            indent = 0
                        if indentmark == 1:
                            nextlinelist = list(line)
                            for value in nextlinelist:
                                if value == '\t':
                                    indent = indent + 8
                                elif value == ' ':
                                    indent = indent + 1
                                elif value != ' ':
                                    break
                            if indent<=indentref:
                                Nodeinfo, index3, node = ifelsecondition(lines, index4, node, Nodeinfo, case)
                                indent = 0
                            else:
                                indent = 0
                    #if 'noc_buffer' in line:
                    #    print(block)
                    #    breakpoint()
                        
                    if ('for (' in line or 'for(' in line) and ('//' not in line.split()[0] and '//' not in line.split()[1]):
                        #breakpoint()
                        if 'begin' not in lines[index4 + 1]:
                            continue
                        recordNode = []
                        for things in Nodeinfo:
                            recordNode.append(things)
                        formark = 1
                        #breakpoint()
                        forline = line.split(';')
                        loopstart = forline[0].replace('for','').replace('(','').replace(' ','').split('=')
                        loopvariable = loopstart[0].replace('int','')
                        for things in parameter:
                            if things.split()[0] in loopstart[1]:
                                loopstart[1] = loopstart[1].replace(things.split()[0],things.split()[1])
                                break
                        try: loopstart[1] = eval(loopstart[1])
                        except: loopstart[1] = 1
                        loopbegin = int(loopstart[1])
                        if '<' in forline[1]:
                            loopend = forline[1].replace(loopvariable,'').replace('<','').replace('=','').replace(' ','')
                        elif '>' in forline[1]:
                            loopend = forline[1].replace(loopvariable,'').replace('>','').replace('=','').replace(' ','')
                        for things in parameter:
                            if things.split()[0] in loopend:
                                loopend = loopend.replace(things.split()[0],things.split()[1])
                                break
                        try:loopend = eval(loopend)
                        except: loopend = 1
                        if 'begin' in lines[index4 + 1]:
                            forbegin = list(lines[index4+1])
                            indentcount = 0
                            for indentx in forbegin:
                                if indentx == ' ':
                                    indentcount = indentcount + 1
                                else:
                                    break
                        
                    elif 'end' in line and formark == 1:
                        endline = list(line)
                        indentend = 0
                        for indent in endline:
                            if indent == ' ':
                                indentend = indentend + 1
                            else:
                                break
                        if indentend == indentcount:
                            formark = 0
                            #breakpoint()
                            if Nodeinfo != recordNode:
                                print('add loop')
                                loopNode = []
                                changenode = 0
                                check = 0
                                #breakpoint()
                                if loopend >= loopbegin:
                                    loop = loopend - loopbegin
                                elif loopbegin > loopend:
                                    loop = loopbegin - loopend
                                for i in range(loop):
                                    
                                    for noderow in Nodeinfo:
                                        if noderow in recordNode:
                                            continue
                                        
                                        elif noderow not in recordNode and check == 0:
                                            changenode = int(noderow[0].split()[0].replace('n',''))
                                            check = 1
                                        loopcondition = []
                                        for node1 in noderow:
                                            newnode =node1.replace(loopvariable + ' ',str(i) + ' ')
                                            for things in parameter:
                                                if things.split()[0] in newnode and '<=' not in newnode:
                                                    newnode = newnode.replace(things.split()[0],things.split()[1])
                                                    break
                                            
                                            newnode = newnode.split()  
                                            #breakpoint()
                                            
                                            newnode1 = ' '.join(newnode)
                                                
                                            newnode1 = newnode1.replace(newnode[0],'n'+str(changenode))
                                            loopcondition.append(newnode1)
                                            changenode = changenode + 1  
                                        loopNode.append(loopcondition)
                                #breakpoint()
                                for noderow in loopNode:
                                    if '==' in noderow[0]:
                                        noderow1 = noderow[0].split()
                                        noderow1.pop()
                                        noderow1.pop(0)
                                        try:xx = eval(' '.join(noderow1))
                                        except: xx = True
                                        #breakpoint()
                                        if not xx:
                                            continue
                                    #breakpoint()
                                    recordNode.append(noderow)
                                #breakpoint()
                                Nodeinfo = recordNode  
                    if 'case' in line and 'endcase' not in line and '//' not in line and ('case(' in line or 'case (' in line):
                        #breakpoint()
                        Nodeinfo, index3, node = casestatement(lines, index4, node, Nodeinfo, ifcond)
    return Nodeinfo, modulelist2
#-------------------------------------

def nodelist(node, nodeavail):
    #breakpoint()
    if type(node) is list:
        for node1 in node:
            nodeavail = nodelist(node1, nodeavail)
        return nodeavail
    elif type(node) is str:
        nodeavail.append(node.split()[0])
        return nodeavail



#---------------------------------------

def nodedistance(node, nodeavail):
    #breakpoint()
    if type(node) is list:
        for node1 in node:
            nodeavail = nodedistance(node1, nodeavail)
        return nodeavail
    elif type(node) is str:
        nodeavail.append(99)
        return nodeavail

def Distance_Evaluation( predecessors3, Nodeflow):

    node_distance = []
    for noderow in Nodeflow:
        for node in noderow:
            if type(node) is list:
                breakpoint()
                node_distance = nodedistance(node, node_distance)
                continue
            node_distance.append(99)
    breakpoint()
    for index, node in enumerate(predecessors3):
        node_distance[int(node.replace('n',''))] = len(predecessors3) - index

    return node_distance

#-----------------------------------------------------

#-----------------------------------------------------


  

#--------------------------------------------------------------

def intconvertor(value):
    if "32'h" in value:
        s1 = value.replace("32'h",'').replace('_','')
        s2 = int(s1,16)
    elif "128'h" in value:
        s1 = value.replace("128'h",'').replace('_','')
        s2 = int(s1,16)
    elif "16'h" in value:
        s1 = value.replace("16'h",'').replace('_','')
        s2 = int(s1,16)
    elif "4'h" in value:
        s1 = value.replace("4'h",'').replace('_','')
        s2 = int(s1,16)
    elif "8'h" in value:
        s1 = value.replace("8'h",'').replace('_','')
        s2 = int(s1,16)
    elif "3'h" in value:
        s1 = value.replace("3'h",'').replace('_','')
        s2 = int(s1,16)
    elif "6'h" in value:
        s1 = value.replace("6'h",'').replace('_','')
        s2 = int(s1,16)
    elif "7'h" in value:
        s1 = value.replace("7'h",'').replace('_','')
        s2 = int(s1,16)
    elif "12'h" in value:
        s1 = value.replace("12'h",'').replace('_','')
        s2 = int(s1,16)
    elif "5'b" in value:
        s1 = value.replace("5'b",'').replace('_','')
        s2 = int(s1,2)
    elif "3'b" in value:
        s1 = value.replace("3'b",'').replace('_','')
        s2 = int(s1,2)
    elif "2'b" in value:
        s1 = value.replace("8'h",'').replace('_','')
        s2 = int(s1,2)
    elif "7'b" in value:
        s1 = value.replace("7'b",'').replace('_','')
        s2 = int(s1,2)
    elif "1'b" in value or "'" in value:
        s1 = value.replace("1'b",'').replace("'",'')
        s2 = int(s1,2)
    return s2  

#-----------------------------------------------------
def checkdefine(flpath,file1):
    Validation = []
    Definevalue = []
    Definevalue1 = []
    checked = []
    #flpath = 'Advanced_Debugger_rtl/'
    with open(flpath + file1) as fl2:
        for line1 in fl2:
            with open(flpath + line1.replace('\n','')) as fl3:
                lines = fl3.readlines()
                fl3.close()
            for index, line in enumerate(lines):
                if "`define" in line:
                    linevalue = line.split()
                    if '//' in linevalue[0]:
                        continue
                    Define = []
                    if 'START' in linevalue[1] and 'ADDR' in linevalue[1]:
                        variable = linevalue[1].split('_')
                        variable1 = " ".join(variable)
                        variable2 = variable1.replace('START','').replace('ADDR','')
                        variable3 = variable2.split()
                        variable = "_".join(variable3)
                        value1 = intconvertor(linevalue[2])
                        Definevalue.append([linevalue[1], linevalue[2]])
                        nextline = lines[index+1]
                        linevalue = nextline.split()
                        value2 = intconvertor(linevalue[2])
                        Define.append(variable)
                        Define.append(value1)
                        Define.append(value2)
                        
                        #--------------------
                        Definevalue1.append(Define)
                    else:
                        if len(linevalue)<3:
                            continue
                        Define.append(linevalue[1])
                        Define.append(linevalue[2])
                        Definevalue.append(Define)

        for index1, address in enumerate(Definevalue1):
            #breakpoint()
            if len(address) < 3:
                continue
            for index2, compare in enumerate(Definevalue1):
                if len(compare) < 3 or index1 == index2 or ([index1,index2] in checked or [index2, index1] in checked):
                    continue
                else:
                    if address[1] > compare[1]:
                        if address[1] > compare[2]:
                            continue
                        else:
                            Validation.append(address[0] + ' and ' + compare[0] + ' address invalid')
                            checked.append([index1, index2])
                    elif address[1] < compare[1]:
                        if address[2] < compare[1]:
                            continue
                        else:
                            Validation.append(address[0] + ' and ' + compare[0] + ' address invalid')
                            checked.append([index1, index2])
    return Validation, Definevalue

#-----------------------------------------------------

def checktopinput(flpath,file1, Valid):
    Input = []
    Inputver = []
    #breakpoint()
    #flpath = 'Advanced_Debugger_rtl/'
    with open(flpath + file1) as fl2:
        for line1 in fl2:
            with open(flpath + line1.replace('\n','')) as fl3:
                lines = fl3.readlines()
                fl3.close()
            for index, line in enumerate(lines):
                if 'input' in line:
                    line = line.replace('\t','').replace('\n','')
                    if 'logic' in line and '[' in line:
                        linevalue = line.split()
                        value1 = linevalue[2].split(':')
                        value2 = value1[0].replace('[','')
                        #breakpoint()
                        if value2.isdigit():
                            Inputver.append( linevalue[3].replace(',','') + ' ' + str(int(value2)+1))
                        else:
                            continue#---------------------fix
                    elif 'logic' in line:
                        linevalue = line.split()
                        Inputver.append( linevalue[2].replace(',','') + ' ' + str(1))
                    else:
                        if '[' in line:
                            linevalue = line.split()
                            value1 = linevalue[1].split(':')
                            value2 = value1[0].replace('[','')
                        #breakpoint()
                            if value2.isdigit():
                                Inputver.append( linevalue[2].replace(',','') + ' ' + str(int(value2)+1))
                            else:
                                continue#---------------------fix
                        else:
                            linevalue = line.split()
                            if len(linevalue) > 2:
                                for i, linevaluex in enumerate(linevalue):
                                    if ',' in linevaluex or ';' in linevaluex:
                                        Inputver.append(linevaluex.replace(',','').replace(';','') + ' ' + str(1))
                            else:
                                Inputver.append(linevalue[1].replace(',','').replace(';','') + ' ' + str(1))

                for value in Input:
                    if 'input' in line and value +  ';' in line:
                        if '[' in line:
                            continue# do something
                        else:
                            Inputver.append( value + ' ' + str(1))
    #breakpoint()
    Input2 = moduleinput(flpath,file1, Valid)
    for val in Input2:
        if val.split()[0] in Inputver:
            continue
        else:
            Inputver.append(val)

    return Input, Inputver

#-----------------------------------------------------

#def checksvinput():
#    Input = []
#    flpath = 'Advanced_Debugger_rtl/'
#    with open(flpath + 'file_list.txt') as fl2:
#        for line1 in fl2:
#            with open(flpath + line1.replace('\n','')) as fl3:
#                lines = fl3.readlines()
#                fl3.close()
#            for index, line in enumerate(lines):
#                if 'input' in line and value +  ',' in line:
#                    line.replace('input','').replace(',','').replace('\n','').replace('logic','').replace('\t','').replace(' ','')
#                    if '[' in line:
#                        Input
#                    else:
#                        Inputver.append( value + ' ' + str(1))
#    return Input, Inputver

#-----------------------------------------------------

def checkconstraint(flpath, file1, Define, Define1):
    Valid = []
    Validreg = []
    for index, IN in enumerate(Define):
        #breakpoint()
        if Define1[index].isdigit():
            #breakpoint()
            x1 = IN + ' = int(' + Define1[index] +')'
            #x = IN.split()[0] + "= int('"+IN.split()[1] +"',2)"
            #try:exec(x)
            #except: #
            exec(x1)
        elif Define1[index] == '""':
            continue 
        else:
            x1 = IN + ' = intconvertor(' + Define1[index] +')'
            x =  IN + '= "' + Define1[index] + '"'
            try: exec(x1)
            except: exec(x)
    #flpath = 'Advanced_Debugger_rtl/'
    with open(flpath + file1) as fl2:
        for line1 in fl2:
            with open(flpath + line1.replace('\n','')) as fl3:
                lines = fl3.readlines()
                fl3.close()
            for index, line in enumerate(lines):
                if 'reg' in line:
                    if '=' in line:
                        line = line.split('=')[0]
                    linevalue = line.split()
                    #breakpoint()
                    if 'reg' == linevalue[0]:
                        #breakpoint()
                        if len(linevalue) > 3 or '][' in line:
                            validreg = []
                            #breakpoint()
                            regsitors = []
                            #if '=' in linevalue:
                            #    regsitors.append(linevalue[1].replace(',','').replace(';',''))
                            for item in linevalue: 
                                
                                if '[' in item:
                                    item1 = item.replace('[','').replace(']','').replace(';','').split(':')
                                    for items in item1:
                                        if items == '0':
                                            continue
                                        else:
                                           try:number = eval(items)
                                           except: continue
                                    validreg.append('[' + str(number) + ':0]')
                                elif ',' in item or ';' in item:
                                    regsitors.append(item.replace(',','').replace(';',''))
                                    
                            validreg = ''.join(validreg)
                            if validreg == '':
                                validreg = str(2)
                            for linevaluex in regsitors:
                                Validreg.append(linevaluex + ' ' + validreg)
                            validreg = []
                        elif len(linevalue)> 2:
                            #breakpoint()
                            l1 = linevalue[1].replace('0','')
                            l2 = l1.replace('[','')
                            l3 = l2.replace(']','')
                            l4 = l3.replace(':','')
                            try:Valid.append(linevalue[2].replace(',','').replace(';','') + ' ' + str(2**(int(l4)+1)))
                            except: continue
                            Validreg.append(linevalue[2].replace(',','').replace(';','') + ' ' + linevalue[1])
                        else:
                            Valid.append(linevalue[1].replace(';','') + ' ' + str(2))
                            Validreg.append(linevalue[1].replace(';','') + ' ' + str(2))
                if 'logic' in line and ('input' not in line and 'output' not in line):
                    linevalue = line.split()
                    #breakpoint()
                    if 'logic' == linevalue[0]:
                        #breakpoint()
                        if len(linevalue) > 3 or '][' in line:
                            validreg = []
                            for item in linevalue: 
                                if '[' in item:
                                    item1 = item.replace('[','').replace(']','').split(':')
                                    for items in item1:
                                        if items == '0':
                                            continue
                                        else:
                                           try:number = eval(items)
                                           except: continue
                                    validreg.append('[' + str(number) + ':0]')
                            validreg = ''.join(validreg)
                            Validreg.append(linevalue[2] + ' ' + validreg)
                            validreg = []
                        elif len(linevalue)> 2:
                            #breakpoint()
                            l1 = linevalue[1].replace('0','')
                            l2 = l1.replace('[','')
                            l3 = l2.replace(']','')
                            l4 = l3.replace(':','')
                            try:Valid.append(linevalue[2].replace(',','').replace(';','') + ' ' + str(2**(int(l4)+1)))
                            except: continue
                            Validreg.append(linevalue[2].replace(',','').replace(';','') + ' ' + linevalue[1])
                        else:
                            Valid.append(linevalue[1].replace(',','').replace(';','') + ' ' + str(2**0))
    return Valid, Validreg
#-----------------------------------------------------

def assign(flpath,file1):
    #flpath = 'Advanced_Debugger_rtl/'
    assignment = []
    with open(flpath + file1) as fl2:
        for line1 in fl2:
            with open(flpath + line1.replace('\n','')) as fl3:
                lines = fl3.readlines()
                fl3.close()
            for index, line in enumerate(lines):
                if 'assign' in line and '=' in line:
                    #breakpoint()
                    value = line.replace('assign','').replace(';','').replace('\n','').replace('//','#').replace('\\','').replace('\t','').replace(' ','')
                    #if '[' not in line:
                    #    for index1, y in enumerate(value):
                    #        if y == '=':
                    #breakpoint()
                    assignment.append(value)
                elif 'always' in line:
                    break
    return assignment

#-----------------------------------------------------

def convertor(value):  
    #breakpoint()  
    if str(value).isdigit():
        s5 = "{0:01b}".format(int(value))
    elif "128'h" in value:
        s4 = value.replace("128'h",'').replace('_','')
        s5 = "{0:0128b}".format(int(s4, 16))
    elif "16'h" in value:
        s4 = value.replace("16'h",'').replace('_','')
        s5 = "{0:016b}".format(int(s4, 16))
    elif "32'h" in value:
        s4 = value.replace("32'h",'').replace('_','')
        s5 = "{0:032b}".format(int(s4, 16))
    elif "4'h" in value:
        s4 = value.replace("4'h",'').replace('_','')
        s5 = "{0:04b}".format(int(s4, 16))
    elif "6'h" in value:
        s4 = value.replace("6'h",'').replace('_','')
        s5 = "{0:06b}".format(int(s4, 16))
    elif "7'h" in value:
        s4 = value.replace("7'h",'').replace('_','')
        s5 = "{0:07b}".format(int(s4, 16))
    elif "12'h" in value:
        s4 = value.replace("12'h",'').replace('_','')
        s5 = "{0:012b}".format(int(s4, 16))
    elif "b" in value:
        s4 = list(value)
        
        while s4[0] != 'b':
            s4.pop(0)
            
        else:
            s4.pop(0)
            s5 = ''.join(s4)
    elif ':' in value:
        s5 = value
    elif "'" in value:
        s5 = value
    else:
        s5 = value

    return s5

#-----------------------------------------------------

def Inputdefine(flpath,file1):
    Define = []
    Definevalue = []
    #flpath = 'Advanced_Debugger_rtl/'
    with open(flpath + file1) as fl2:
        for line1 in fl2:
            with open(flpath + line1.replace('\n','')) as fl3:
                lines = fl3.readlines()
                fl3.close()
            for index, line in enumerate(lines):
                if '`define' in line:
                    value = line.split()
                    if '//'in value[0] or len(value)<3 or ')' in value[2] or ')' in value[1]:
                        continue
                    if value[2].isdigit():
#---------------------------------------------------
                        Define.append(value[1])
                        Definevalue.append(value[2])
                elif 'parameter' in line:
                    value = line.split()
                    #if value
                        
                    if 'unsigned' in value:
                        Define.append(value[3])
                        Definevalue.append(value[5].replace(',','').replace(';',''))
                    elif value[0] == '//':
                        continue
                    elif '[' in value[1]:
                        #breakpoint()
                        for index, value1 in enumerate(value):
                            if ']' in value1:
                                Define.append(value[index+1])
                                Definevalue.append(value[index+3].replace(',','').replace(';',''))
                    elif 'bit' == value[1]:
                        Define.append(value[2])
                        Definevalue.append(value[4].replace(',','').replace(';',''))
                    else:
                        Define.append(value[1])
                        Definevalue.append(value[3].replace(',','').replace(';',''))
                    
    return Define, Definevalue

#-----------------------------------------------------

def variablebondary(Valid, Nodeflow):

    breakpoint()
    Validvalue = []
    x = raw_input('Any bondary need to add?(y/n)')
    while x != 'n':
        if x != 'y':
            print('Input error')
            x = raw_input('Any bondary need to add?(y/n)')
            continue
        combination = []
        for Noderow in Nodeflow:
            for Node in Noderow:
                print(Node)
        y = raw_input('pick an input: ')
        check = 0
        for value in Valid:
            if y == value.split()[0] or value.split()[0] in y:
                yvalue = raw_input('Please add the value of bondary: ')
                if yvalue.isdigit():
                    constraint = y + " " + yvalue
                    Validvalue.append(constraint)
                    check = 1
                    breakpoint()
                    x = raw_input('Any constraint need to add?(y/n)')
                    break
        if check == 0:
            print('Input error')
            x = raw_input('Any constraint need to add?(y/n)')
  #  else: 
  #      print('Input error')
  #      x = raw_input('Any constraint need to add?(y/n)')               

    return Validvalue
    
#-----------------------------------------------------

def moduleinput(flpath,file1, Valid):
    Input = []
    with open(flpath + file1) as fl2:
        for line1 in fl2:
            with open(flpath + line1.replace('\n','')) as fl3:
                lines = fl3.readlines()
                fl3.close()
            for index, line in enumerate(lines):
                if '.' in line and '(' in line and ')' in line:
                    for val in Valid:
                        #breakpoint()
                        if val.split()[0] in line and '(' in line and ')' in line and ('_i' not in line or '_o' in line):
                            check = 0
                            valuex = line.split()
                            for IN in valuex:
                                if IN == val.split()[0]:
                                    check = 1
                                    break
                            #breakpoint()
                            if check == 1:
                                length = np.log2(int(val.split()[1]))
                                if int(length) == 0:
                                    Input.append(val.split()[0]+ ' '+ str(1))
                                else:
                                    Input.append(val.split()[0]+ ' '+ str(int(length)))
                    
    return Input


#-----------------------------------------------------

def Constraintproperty(Input,Nodeflow):
    breakpoint()
    Validvalue = []
    x = raw_input('Any constraint need to add?(y/n)')
    while x != 'n':
        if x != 'y':
            print('Input error')
            x = raw_input('Any constraint need to add?(y/n)')
            continue
        Typ = raw_input('Input or Process Constraint?(input/process) ')
        if Typ == 'input':
            check = 0
            combination = []
            for index, value in enumerate(Input):
                print(value)
            y = raw_input('pick an input: ')
            for value in Input:
                if y == value:
                    check = 1 
                
            if check == 1:
                yvalue = raw_input('Please add the value of constraint: ')
                constraint = y + " " + yvalue
                combination.append(constraint)
                for Noderow in Nodeflow:
                    for Node in Noderow:
                        print(Node)
                        #breakpoint()
                check = 0
                z = raw_input('Pick a variable in node: ')
                for Noderow in Nodeflow:
                    for Node in Noderow:
                        if z == Node.split()[1] or Node.split()[1] in z:
                            check1 = 1
                if check1 == 1:
                    zvalue = raw_input('Please add the value of constraint: ')
                    constraint1 = z + " " + zvalue
                    combination.append(constraint1)
                    Validvalue.append(combination)
                    breakpoint()
                else:
                    print('Input error')
                x = raw_input('Any constraint need to add?(y/n)')
            else: 
                print('Input error')
                x = raw_input('Any constraint need to add?(y/n)')
                
        elif Typ == 'process':
            check = 0
            combination = []
            for Noderow in Nodeflow:
                for Node in Noderow:
                    print(Node)
                    #breakpoint()
            y = raw_input('Pick a variable in node: ')
            for Noderow in Nodeflow:
                for Node in Noderow:
                    if y == Node.split()[1] or Node.split()[1] in y:
                        check1 = 1
                    
            if check1 == 1:
                yvalue = raw_input('Please add the value of constraint: ')
                constraint = y + " " + yvalue
                combination.append(constraint)
                check = 0
                for Noderow in Nodeflow:
                    for Node in Noderow:
                        print(Node)
                        #breakpoint()
                z = raw_input('Pick a variable in node: ')
                for Noderow in Nodeflow:
                    for Node in Noderow:
                        if z == Node.split()[1]:
                            check1 = 1
                if check1 == 1:
                    zvalue = raw_input('Please add the value of constraint: ')
                    constraint1 = z + " " + zvalue
                    combination.append(constraint1)
                    Validvalue.append(combination)
                    breakpoint()
                else:
                    print('Input error')
                x = raw_input('Any constraint need to add?(y/n)')
            else: 
                print('Input error')
                x = raw_input('Any constraint need to add?(y/n)')
        else:
            print('Input error')
            x = raw_input('Any Constraint need to add?(y/n)')


    return Validvalue
#-----------------------------------------------------

def decidepredecessor(Nodeflow, predecessors3):
    xx = []
    print('Nodeflow:')
    for noderow in Nodeflow:
        for node in noderow:
            print(node)
    print('Predecessors: ')
    for pre in predecessors3:
        print(pre)
    x = raw_input('Choose a node in predecessors or no: ')
    while x != None:
        if x in predecessors3:
            xx.append(x)
            #x = raw_input('Choose another node in predecessors or no: ')
            #continue
            return x
        elif x == 'no':
            return    
        elif x not in predecessors3:
            print('Node not in predecessors:')
            x = raw_input('Choose a node in predecessors or no: ')

#---------------------------------------------------------------------------

def checkconstraint2(simIn, Constraint):
    Validation = []
    for index, IN in enumerate(simIn):
        if IN.split()[1].isdigit():
            x = IN.split()[0] + ' = int(valueconvertor("' + IN.split()[1] + '"),2)'
            exec(x)
        elif "'h" in IN.split()[1]:
            x = IN.split()[0] + ' = ' + 'convertor(IN.split()[1])'
            exec(x)
        else:
            x = IN.split()[0] + ' = ' + '"' + IN.split()[1] + '"'
            exec(x)
    for index2, val in enumerate(Constraint):
        breakpoint()
        x = str( val[0].split()[0]) + ' == ' + str(val[0].split()[1])
        x1 = str(val[0].split()[0]) + ' == ' + '"' + val[0].split()[1] + '"'
        try : match = eval(x)
        except: match = eval(x1)
        if match:
            x = val[1]#.split()[0] + ' == ' + str(val[1].split()[1])
            match1 = eval(x)
            if match1:
                continue
            elif not match1:
                valid = val[0].split()[0] + ' == ' + str(val[0].split()[1]) + ', ' + val[1].split()[0] + ' == ' + str(val[1].split()[1]) + '/Constraint not matched'
                #breakpoint()
                Validation.append(valid)
    return Validation

#-----------------------------------------------------
def checkval(simIn, Valid, Constraint, Property, pathindex):
    Val = []
    #breakpoint()
    for index1, sim in enumerate(simIn):
        for index2, val in enumerate(Valid):
            if simIn[index1].split()[0] in val:
                #breakpoint()
                if simIn[index1].split()[1].isdigit():
                    value = str(simIn[index1].split()[1])
                    try :value1 = int(valueconvertor(value),2)
                    except: value1 = value
                    if int(value1) >= int(Valid[index2].split()[1]):
                        Val.append(simIn[index1].split()[0] + ' overflow invalid ' + str(int(Valid[index2].split()[1]) - 1) + ' but ' + str(value1))
                else:
                    continue
    Val1 = checkconstraint2(simIn, Constraint)
    if Val1 != []:
        Val.append(Val1)
    return Val

#-----------------------------------------------------

def hexcalculation(value1, value2):
    ss = int(value1,2) + int(value2.replace("4'h",''),16)
    value = "{0:04b}".format(ss)
    return value    

def hexreplacement(ovalue , nvalue, string):

    olist = list(ovalue)
    nlist = list(nvalue)
    slist = list(string)
    
    for index, val in enumerate(slist):
        if '[' in val:
            i = 1
            ivalue = []
            while slist[index + i] != ':':
                ivalue.append(slist[index + i])
                i = i + 1
            #breakpoint()
            value1 = int(''.join(ivalue))
        if ':' in val:
            i = 1
            ivalue = []
            while slist[index + i] != ']':
                ivalue.append(slist[index + i])
                i = i + 1
            value2 = int(''.join(ivalue))

    value = []
    for index, val in enumerate(olist):
        if index == value1:
            i = 0
            j = value1
            #breakpoint()
            while j != value2:
                value.append(nlist[i])
                i = i + 1
                j = j + 1
            
        elif index < value1 or index >= value2:
            value.append(olist[index])
    value = ''.join(value)
    return value

def hextovariable(line):
    s = list(line)
    info = []
    for index, char in enumerate(s):
        #breakpoint()
        info.append(char)
        if char == '[':
            info.pop()
            info = ''.join(info)
            orignial = info
            i = 1 
            information = []
            while s[index + i] != ']':
                information.append(s[index+i])
                i = i + 1
            value = ''.join(information)
            value1 = value.split(':')
            value2 = int(value1[0])+1
            value3 = int(value1[1])
            info = info + '[' +str(value3) +':' + str(value2) + ']'
            break                    
            
    return info, orignial

def valueconvertor(value):
    value1 = list(value)
    value2 = []
    for index in reversed(range(len(value1))):
        value2.append(value1[index])
    value2 = ''.join(value2)
    return value2

def valueconvertor2(simIn, Valid):
    for index, value in enumerate(Valid):
        for index1,value1 in enumerate(simIn):
            if value1.split()[0] == value.split()[0]:
                length = np.log2(int(value.split()[1]))
                x = 'value2 = "{0:0' + str(int(length)) + 'b}".format(int(value1.split()[1]))'
                #breakpoint()
                
                exec(x)
                replacement = value1.split()[0] + ' ' + value2
                simIn.pop(index1)
                simIn.insert(index1, replacement)
    return simIn

def hexadjustment(value):
    value1 = value.split()[0]
    list1 = list(value1)
    val1 = []
    val2 = []
    for index, val in enumerate(list1):
        if val == '[':
            i = 1
            val3 = list1[index + i]
            while val3 != ':':
                val1.append(val3)
                i = i + 1
                val3 = list1[index + i]
            else:
                val1 = ''.join(val1)
        elif val == ':':
            i = 1
            val3 = list1[index + i]
            while val3 != ']':
                val2.append(val3)
                i = i + 1
                val3 = list1[index + i]
            else:
                val2 = ''.join(val2)
    value2 = int(val2) - int(val1)
    x = "{0:0"+ str(value2) + "b}"
    value4 =     x.format(int(value.split()[1], 2))
    value3 = value1 + ' ' + value4
    return value3

def Binaryaddition(value):
    linevalue = value.split('=')
    value1 = linevalue[1]
    value2 = value1.split(',')
    newstring = []
    for index, val in enumerate(value2):
        newstring.insert(0,val)
    for index, val in enumerate(newstring):
        if ':' in val:
            val1 = val.replace('{','').replace('}','')
            variable1, variable2 = hextovariable(val1)
            newstring[index] = variable1
            continue
        elif val.count('{') >= 2:
            addon = []
            val1 = val.replace(' ','').split('{')
            for valx in val1:
                #breakpoint()
                if valx == '':
                    continue
                elif valx.isdigit():
                    mux = valx
                else:
                    chara = valx.replace('}','')
            for x in range(int(mux)):
                addon.append(chara)
            newstring[index] = '+'.join(addon)        
            continue
        elif "'b" in val:
            addon = []
            val1 = val.replace(' ','').replace('{','').replace('}','').split("'b")
            #breakpoint()
            for x in range(int(val1[0])):
                addon.append(val1[1])
            val2 = ''.join(addon)
            newstring[index] = "'" + val2 + "'"
            continue
        elif "'h" in val:
            addon = []
            val1 = val.replace(' ','').replace('{','').replace('}','').split("'h")
            #breakpoint()
            for x in range(int(val1[0])):
                addon.append(val1[1])
            val2 = ''.join(addon)
            newstring[index] = "'" + val2 + "'"
            continue
        else:
            val1 = val.replace('{','').replace('}','')
            newstring[index] = val1
            continue            
    #breakpoint()
    string = '+'.join(newstring)
    return string


def Model_check(module, always, lines):
    bug = 0
    Check = []
    if always == []:
        return
    always1 = always[0].replace('always','')
    always = always1.split()
    always = ' '.join(always) + ' 0'
    if 'True' not in always:
        Check.append(always)
    #lines = 
    for flow in module:
        flow = flow.split()
        flow.pop(0)
        flow = ' '.join(flow)
        Check.append(flow)
    #if "n27 activeroute <= {{CHANNELS-1{1'b0}},1'b1}; 1" in module:
    #    print(module)
    #    breakpoint()
    for line1 in lines:
        stop = 0
        checkalways = 0
        line1 = line1[0]
        line1 = line1.split(';')
        checkline = []
        for indexx,line in enumerate(line1):
            #check = 0
            linex1 = int(line.split()[len(line.split())-1])
            try: linexx = line1[indexx + 1].split()[len(line1[indexx + 1].split())-1]
            except: linexx = -1
            #if indexx == 0:
            #    check  = int(linex1)
            if int(linexx) == linex1 and indexx != len(line1) - 1:
                checkline.append(line[:(len(line)-1)])
                
            elif linexx > linex1 or linexx == -1:
                #if checkline == []:
                checkline.append(line[:(len(line)-1)])
                #elif indexx == len(line1) - 1:
                #    checkline.append(line[:(len(line)-1)])
                #checkline1 = []
                for index1 ,flow in enumerate(Check):
                    match = 0
                    checkline1 = []
                    if index1 < stop:
                        continue
                    flow = flow.replace(';','')
                    linex2 = int(flow.split()[len(flow.split())-1])
                    try: linexx2 = Check[index1 + 1].split()[len(Check[index1 + 1].split())-1]
                    except: linexx2 = -1
                    #if index1 == 0:
                    #    check1  = int(linex2)
                    if int(linexx2) == linex2 and index1 != len(Check) - 1:
                        checkline1.append(flow[:(len(flow)-1)])
                    elif linexx2 > linex2 or linexx2 == -1:
                        
                        #if checkline1 == []:
                        checkline1.append(flow[:(len(flow)-1)])
                        #elif index1 == len(Check) - 1:
                        #    checkline1.append(flow[:(len(flow)-1)])
                        stop = index1
                        if '==' in checkline[0]:
                            #breakpoint()
                            check = 0
                            for things in checkline1:
                                for thing in checkline:
                                    flow1 = things.split('==')
                                    variable1 = thing.split('==')
                                    if flow1[0].replace(' ','') == variable1[0].replace(' ',''):
                                        if flow1[1].replace(' ','') == variable1[1].replace(' ',''):
                                            check = check + 1
                                            break
                                    elif flow1[0].replace(' ','') != variable1[0].replace(' ',''):
                                        continue
                            if check == len(checkline):
                                match = 1
                            else:
                                match = 0
                                
                        elif '<=' in checkline[0]:
                            check = 0
                            assign = 0
                            for things in checkline:
                                for thing in checkline1:
                                    flow1 = things.split('<=')
                                    variable1 = thing.split('<=')
                                    if flow1[0].replace(' ','') == variable1[0].replace(' ',''):
                                        assign = assign + 1
                                        if variable1[1] == flow1[1]:
                                            check = check + 1
                                        elif match == 1 and variable1[1].replace(' ','') != flow1[1]:
                                            bug = 1
                                            breakpoint()
                                            return bug
                                    else:
                                        continue
                            if match == 0 and check == len(checkline):
                                bug = 1
                                breakpoint()
                                return bug
                            #if 
                            #    continue
                            elif assign >= 1 and check >= 1 and check < len(checkline):
                                bug = 1
                                breakpoint()
                                return bug
                        checkline1.append(flow[:(len(flow)-1)])
                checkline.append(line[:(len(line)-1)])
            
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
print(specline)
breakpoint()

flpath = 'ram/'
file1 = 'file_list.txt'
#Nodeflow, Nodeflownew = RealiCFG(flpath, file1)
predecessors = []
predecessors2 = []
predecessors4 = []
#breakpoint()

#Nodeflow1 = Nodeflow_reset(Nodeflow)
#Nodeflownew1 = Nodeflow_reset(Nodeflownew)


#breakpoint()
#print(Nodeflownew1)

nodetoreach = []
#for item in Nodeflownew1:
#    if len(item) > 1:
#        for nodes in item:
#            if '<=' in nodes:
#                node = nodes.split()
#                nodetoreach.append(node[0])

flpath1 = 'RTL/All_RTL/'
with open(flpath1 + "RTLFiles.txt") as fl:
        #breakpoint()
        moduleline = fl.readlines()
        fl.close()

for index, i in enumerate(moduleline):
    modulenumber = index+ 1

Allmodules = []
number = 0
#breakpoint()
for i in range(modulenumber):
    file2 = "RTLFiles_" + str(i) + ".txt"
    moduleNodeflow, moduleNodeflownew = RealiCFG(flpath1, file2)
    #breakpoint()
    Nodeflowx = Nodeflow_reset(moduleNodeflownew)
    print(Nodeflowx)
    #breakpoint()
    
    if Nodeflowx not in Allmodules:
        Allmodules.append(Nodeflowx)
        #breakpoint()
        with open('Extracted_CFG_' + str(number) + '.txt', 'w+') as fl:
            for linex in Nodeflowx:
                if isinstance(linex,str):
                    fl.write(linex + '\n')
                else:
                    for line in linex:
                        fl.write(line + '\n')
            fl.close()
        number = number + 1
    



print('---------------------done with modules---------------------')
breakpoint()

 
breakpoint()   



