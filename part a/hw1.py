#hw1.py -- HW1DB, simple database implementation in python. a CLI that interfaces with csv files given as arguments
#Caroline Roig-Irwin clr2176
#CS 4111 Assignment 1a

import sys
import csv

metas = {'orders': ['orders.csv','OrderID'], 'customers': ['customers.csv','CustomerID']}  #contains filename->csv/AK mapping

#parse and return columns given in a string of either key=value or value1,value2...valueN
#given that columns are comma-separated but values may have commas enclosed in quotations 
#and there may be other delimiters (i.e. key=value) at play that must be kept in place
#(i.e. this is for the situations in which string.split() and csv.DictReader will not parse
#correctly and cleanly)
def parseColumns(columns,kv=True):
    spl = columns.split(',')
    ans = [spl[0]]
    for x in range(1,len(spl)):
        #generally, we will add the next element in a comma-separated list to the return value.
        #however, if the previous element is non-empty, does not end with a closing quote,
        #and either begins with a quote (value list) or has an equal sign followed by a 
        #quote (key="value") then we will assume that the next element was split erroneously
        #and contains a literal comma, so will append the literal comma and the next element
        #to the end of the previous element.
        if len(ans[-1]) > 0 \
        and ans[-1][-1] != '\"' and ('=\"' in ans[-1] \
        or (not kv and ans[-1][0] == '\"')):
            ans[-1] = ans[-1] + ',' + spl[x]
        else: 
            ans.append(spl[x])
    return ans

#make sure column names you are searching for in a csv actually exist in the file
def checkColumnNames(tablename, columns):
    with open(metas[tablename][0]) as table:
        r = csv.DictReader(table)
        head = r.next()
        for c in columns:
            try:
                val = head[c]
            except KeyError:
                print >> sys.stderr, 'ERROR: ' + c + ' is not a column of table ' + tablename
                return False
    return True

#find function. given a tablename and columns in a string of key=value pairs,
#separated by commas, parse the column names and check format, then open the
#given table and check all rows for matches to the values
def find(tablename, cols):
    colvals = parseColumns(cols)
    cvs = dict()
    for val in colvals:
        try:
            [name,value] = val.strip().split('=',1)
            if name in cvs: 
                print >> sys.stderr, 'ERROR: cannot have two values for the same column'
                return
            cvs[name] = value
        except ValueError:
            print >> sys.stderr, 'ERROR: please specify columns in the form of column1=value1'
            return #non-fatal
            
    if not checkColumnNames(tablename,cvs.keys()):
        #returned false, must be error
        return
         
    with open(metas[tablename][0]) as table:
        r = csv.DictReader(table)
        for row in r:
            match = True
            for k in cvs:
                if row[k] != cvs[k].strip('\"'):
                    match = False
                    break
            if match: print row
   

#insert function. given data, checks for non-null primary key that does not exist in tablename
#and correct number of columns listed in data as (value1,value2...valueN). Appends data 
#to the end of the file if it is determined it can be inserted.     
def insert(tablename, data):
    if data[0] != '(' or data[-1] != ')':
        print >> sys.stderr, 'ERROR: data incorrectly specified, please enter \'insert <tablename> \
(column1,...columnN)\' '
        return
    pcols = parseColumns(data.strip('()'),False) #parsed 
    if pcols[0].strip('\" \t\n').upper() in ('','NULL') :
        print >> sys.stderr, 'ERROR: null or empty primary key, could not insert.'
        return
        
    with open(metas[tablename][0]) as table:
        r = csv.DictReader(table)
        ncols = len(r.next())
        if ncols != len(pcols):
            print >> sys.stderr, 'ERROR: Data does not contain correct amount of columns'
            return
        table.seek(0) #return to the beginning
        for row in r:
            if row[metas[tablename][1]] == pcols[0].strip('\"'):
                print >> sys.stderr, 'ERROR: Could not insert. Data for this primary key already exists'
                return
    
    #non-empty, non-taken primary key, correct number of columns.
    with open(metas[tablename][0],'a') as table:
        actualData = ''
        for colu in pcols: actualData += colu.strip() + ','
        table.write(actualData[:-1])
        table.write('\n')
    print 'successfully inserted data'


#receive command-line input
while 1:
    x = raw_input("HW1DB> ").strip()
    if x.upper() == 'EXIT': 
        sys.exit(0) #successful exit, do not return an error code
    splits = x.split(' ',2)
    if splits[0].upper() not in ['FIND','INSERT'] or len(splits) != 3: 
        print >> sys.stderr, 'ERROR: command not recognized'
        continue
    if splits[1] not in metas:
        print >> sys.stderr, 'ERROR: table ' + splits[1] + ' does not exist'
        continue
    #print splits
    if splits[0].upper() == 'FIND':
        find(splits[1],splits[2])
    else: 
        insert(splits[1],splits[2])

    
    
    
    
    
    
    
    
    
    
    
    
    