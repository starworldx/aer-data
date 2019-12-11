'''

'''
#! python3

import sys, requests, re, time, os
from datetime import date, datetime, timedelta

now = datetime.now()
dateNow = str(now.day) + "-" + now.strftime("%B")[0:3] + "-" + str(now.year)[2:4]
dateNowToPrint = ("%s-%02d-%02d")%(now.year,now.month,now.day)
csvFileData = "data.csv"
csvFileLic = "licence.csv"

#licence = "Daily File Downld/WELLS0301.TXT"
# RUN THIS FILE AS ADMIN

def getFile(fileName):
    url = "http://www.aer.ca/data/well-lic/" + fileName
    res = requests.get(url)
    res.raise_for_status()
    f = open('Daily File Downld\\' + fileName, 'wb')
    for char in res:
        f.write(char)
    f.close()
    
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def crHeads(licence,csvFile,csvFile2):
    with open(licence, 'r') as li:
        head = re.findall(r'(WELL\sNAME)\s.+(LICENCE\sNUMBER)\s.+(MINERAL\sRIGHTS)\s+(GROUND\sELEVATION)\s+\n\s+(UNIQUE\sIDENTIFIER)\s+(SURFACE\sCO-ORDINATES)\s+(BOARD\sFIELD\sCENTRE)\s+(PROJECTED\sDEPTH)\s+\n\s+(LAHEE\sCLASSIFICATION)\s+(FIELD)\s+(TERMINATING ZONE)\s+\n\s+(DRILLING\s+OPERATION)\s+(WELL\sPURPOSE)\s+(WELL\s+TYPE)\s+(SUBSTANCE)\s+\n\s+(LICENSEE)\s+(SURFACE\sLOCATION)\s+\n\s+---',li.read())
        for h in head:
            h=['DATE'] + list(h) +['AMENDED UWI','FIELD AMENDED','AMENDMENT VALUE']
            g = str(h[0]) + "," + str(h[1]) + "," + str(h[2]) + ","+ str(h[3]) + ","+ str(h[4]) + ","+ str(h[5]) + ","+ str(h[6]) + ","+ str(h[7]) + ","+ str(h[8]) + ","+ str(h[9]) + ","+ str(h[10]) + ","+ str(h[11]) + ","+ str(h[12]) + ","+ str(h[13]) + ","+ str(h[14]) + ","+ str(h[15]) + ","+ str(h[16])+ ","+ str(h[17])+ ","+ str(h[18])+ ","+ str(h[19])
        with open(csvFile,'w') as go:
            go.write(g + "\n")

    with open(csvFile2, 'w') as golic:
        licHead = ['DATE','AMENDED WELL','AMENDMENT LICENCE','AMENDED WELLUID','AMENDED UWI','WELL NAME']
        licP = str(licHead[0]) + "," +str(licHead[1]) + "," +str(licHead[2]) + "," +str(licHead[3]) + "," +str(licHead[4])+ "," +str(licHead[5])
        golic.write(licP + "\n")

def gogoToall(licenceF,dateFile,csvFile,csvFile2):
    with open(licenceF, 'r') as li:
        licData = li.read()
        fields = re.findall(r'\n\s+(\S.+)?\s+(\d+)\s+(\S+\s\S+|\S+)\s+(\d+\.\dM|\d+M)\s+\n\s+(\S+)\s+(\S\s+\d+.\dM\s\s\S\s+\d+.\dM)\s+(\S+\s\S+|\S+)\s+(\d+\.\d)M\s+\n\s+(\S+\s\(.+\))\s+(\S+\s\S+|\S+)\s+(\S+.+)\n\s+(\S+)\s+(DOMESTIC|TRAINING|INJECTION|UNDEFINED|NEW|RESUMPTIONPRODUCTION|RESUMPTIONOBSERVATION|RESUMPTION)\s+(OBSERVATION|INJECTION|OIL\sSAND\sEVALUATION|PRODUCTION\s\(SCHEME\)|\(\SCHEME\)\|PRODUCTION|\S+|\s)\s+(NONE|.+)\n\s+(.+)\s{3}\s+(\d+\-\d+\-\d+\-\S+)', licData)
        fields2 = re.findall(r'\n\s+(\S.+)\s(\d{7})\s+UWI\:\s+(\S+)\s+(\S+)\s+WELL\sNAME\:\s+(\S.+)\s|\n\s+(\S.+)\s(\d{7})\s+UWI\:\s+(\S+)\s+(\S+)(\s)',licData)
        with open(csvFile,'a') as csv:
            f1 = []
            for val in fields:
                valStriped = []
                val=list(val)

                if str(val[12]) == 'RESUMPTIONPRODUCTION':
                    val[12] = 'RESUMPTION'
                    val[13] = 'PRODUCTION ' + val[13]
                elif str(val[12]) == 'RESUMPTIONOBSERVATION':
                    val[12] = 'RESUMPTION'
                    val[14] = val[13]
                    val[13] = 'OBSERVATION'
                elif 'NONE' in str(val[13]):
                    val[14] = 'NONE'
                    val[13] = 'OBSERVATION '
                else:
                    print (".")

                for v in val:
                    v=v.rstrip()
                    valStriped.append(v)

                a = dateFile + ","  + str(valStriped[0]) + "," + str(valStriped[1]) + "," + str(valStriped[2]) + ","+ str(valStriped[3]) + ","+ str(valStriped[4]) + ","+ str(valStriped[5]) + ","+ str(valStriped[6]) + ","+ str(valStriped[7]) + ","+ str(valStriped[8]) + ","+ str(valStriped[9]) + ","+ str(valStriped[10]) + ","+ str(valStriped[11]) + ","+ str(valStriped[12]) + ","+ str(valStriped[13]) + ","+ str(valStriped[14]) + ","+ str(valStriped[15]) + ","+ str(valStriped[16]) + "\n"
                sheet1 = [dateFile] + valStriped
                f1.append(sheet1)
                csv.write(a)
        with open(csvFile2,'a') as csv2:
            f2 = []
            for val2 in fields2:
                val2 = list(val2)
                val2Striped = []
                for v in val2:
                    v=v.rstrip()
                    val2Striped.append(v)
                f2.append(val2Striped)
                if val2[0] != '':
                    b = dateFile + "," + str(val2[0]) + "," + str(val2[1]) +"," +str(val2[2]) + "," + str(val2[3])+ "," + str(val2[4])+ "\n"
                else:
                    b = dateFile + "," + str(val2[5]) + "," + str(val2[6]) +"," +str(val2[7]) + "," + str(val2[8])+ "," + str(val2[9])+ "\n"
                csv2.write(b)
                time.sleep(1)

def periodtoUpdate():
    ''' 
    This function will find the last successful download and processing of the TEXT files from log file, Tell user the date of last update and ask user if they would like to update the database? Then use the current date to find period and pass all dates that reqire download to getOne() in a list format. 
    
    '''
    pass

def getOne():
    result = input("\n Enter date in format YYYY-MM-DD for today '" + dateNowToPrint + "' :")
    fileN = "WELLS" + str(result)[5:7] + str(result)[8:] + ".TXT"
    getFile(fileN)
    if os.path.isfile(csvFileLic) and os.path.isfile(csvFileData):
        gogoToall("Daily File Downld\\" + fileN, str(result),csvFileData,csvFileLic)
    else:
        crHeads(fileN, csvFileData,csvFileLic)
        time.sleep(5)
        gogoToall("Daily File Downld\\" + fileN, str(result),csvFileData,csvFileLic)

if __name__ == "__main__":
    
    if not os.path.exists(os.path.join(os.getcwd(), 'Daily File Downld')):
        os.makedirs(os.getcwd()+"\Daily File Downld")
    
    getOne()
