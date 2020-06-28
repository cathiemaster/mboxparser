import base64, re, os
import dominate
import dominate.tags as tags 
from collections import defaultdict

''' 
    printFile: Prints file data
'''
def printFile(filename):
    i = 0
    for line in filename:
        if (i < 10): 
            print(line)
            i += 1

'''
    writeToFile: Writes message data to file
'''
def writeToFile(messages, imgFileNames, filename):
    fileNum = 0

    for (name, number) in messages:
        dirName = getFullname(name)
        newDir = os.getcwd() + "/" + dirName[:-1]

        if (os.path.isdir(newDir) is False):
            try:    
                os.mkdir(dirName[:-1])
            except:
                print("Unable to make folder for " + name)
        try:
            os.chdir(newDir)
        except: 
            print("Unable to access folder: " + newDir)

        #print(os.getcwd())
        
        fname = dirName[:-1] + "_" + str(number) + "_" + str(fileNum) + ".html"
        msgList = messages[(name, number)]
        #print(msgList)
        #getHTML(name, number, msgList, fname)     

'''
    parseFile: Parses given .mbox file and outputs the resulting dictionary storing message data 
'''
def parseFile(fp, filename):
    name = status = weekday = date = msg = msgType = imgStr = imgName = ""
    number = imgCtr = msgCtr = 1 
    flag = False
    imgFileNames = []
    msgDict = defaultdict(list)

    print("Creating directory for images")
    dirPath = os.getcwd() + "/Images"
    if (os.path.isdir(dirPath) is False):
        try:
            os.mkdir("Images")
        except:
            print("Unable to create directory for images")
    
    print("Parsing Filename: " + filename)
    for line in fp:
        (regexp, version)= getRegexp(line)

        if (regexp is not None):
            #print(line)
            if (regexp.group(1) == "From: "): 
                status = "R"
                name = ""
                name = regexp.group(2)

                if (version == 1):
                    number = int(regexp.group(3) + regexp.group(4) + regexp.group(5))
                elif (version == 2):
                    number = int(regexp.group(3))

            elif (regexp.group(1) == "To: "):
                #status = ""
                status = "S"
                name = ""
                name = regexp.group(2)

                if (version == 1):
                    number = int(regexp.group(3) + regexp.group(4) + regexp.group(5))
                elif (version == 2):
                    number = int(regexp.group(3))

            elif (regexp.group(1) == "Date: "):
                #print(regexp)
                date = ""
                weekday = regexp.group(2)
                
                if ((int(regexp.group(3)) >= 1) and 
                    (int(regexp.group(3)) <= 9)):
                    day = "0" + regexp.group(3)
                else:
                    day = regexp.group(3)

                date = getMonthNum(regexp.group(4)) + "-" + day + "-" + regexp.group(5)
            elif (regexp.group(1) == "Content-Transfer-Encoding: quoted-printable"):
                msg = ""
                msg = getMsg(fp)
                flag = True
                #print(msg)
            elif (regexp.group(1) == "Content-Type: "):
                msgType = ""
                imgStr = ""
                if (regexp.group(2) == "text/plain"):
                    msgType = "SMS"
                elif ((regexp.group(2) == "image/jpeg") or (regexp.group(2) == "image/png") or (regexp.group(2) == "image/gif")):
                    imgStr = getMMSStr(fp)
                    imgName = decodeMMS(name, number, imgStr, imgCtr, regexp.group(2), dirPath)
                    imgFileNames.append(imgName)
                    imgCtr += 1

                    msgType = "MMS"
                    flag = True

            '''
                Add message to message dictionary
            '''
            if (flag is True):
                if (msgType == "SMS"):
                    msgData = (date, status, msgType, msg)
                    msgDict[(name, number)].append(msgData)
                else: 
                    msgData = (date, status, msgType, imgName)
                    #print(name)
                    msgDict[(name, number)].append(msgData)   

                msgCtr += 1
                flag = False
 
    #msgDict.pop(("", 1))
    #print(msgDict)
    return (msgDict, imgFileNames)               

""" 
    getRegexp: Parses line using regexps to determine contact info, datetime, and message data 
"""
def getRegexp(line):
    # Contact info - Message Recieved, format 1
    regexp = re.search("^(From: )([a-zA-Z]+ [a-zA-Z]+) <\D([0-9]+)\D ([0-9]+)-([0-9]+).*$", line)
    version = 1

    # Contact info - Message Received, format 2
    if (regexp is None): 
        regexp = re.search("^(From: )([a-zA-Z]+ []a-zA-z]+) <\+([0-9]{10,11})@([a-z]*).([a-z]*)>$", line)
        version = 2

    # Contact info - Message Sent, format 1
    if (regexp is None):
        regexp = re.search("^(To: )([a-zA-Z]+ [a-zA-Z]+) <\D([0-9]+)\D ([0-9]+)-([0-9]+).*$", line)
        version = 1

    # Contact info - Message Sent, format 2
    if (regexp is None):
        regexp = re.search("^(To: )([a-zA-Z]+ []a-zA-z]+) <\+([0-9]{10,11})@([a-z]*).([a-z]*)>$", line)
        version = 2

    # Datetime info
    if (regexp is None):
        regexp = re.search("^(Date: )([a-zA-Z]+), ([0-9]+) ([a-zA-Z]+) ([0-9]{4}) ([0-9]{2}:[0-9]{2}:[0-9]{2}).*$", line)
        version = -1

    # Message info 
    if (regexp is None):
        regexp = re.search("^(Content-Transfer-Encoding: quoted-printable).*$", line)
        version = -1

    # Content type info 
    if (regexp is None):
        regexp = re.search("^(Content-Type: )([a-z]+/[a-z]+).*$", line)
        version = -1

    return (regexp, version)

'''
    getMsg: Extracts message from input file
'''
def getMsg(fp): 
    regexp = "^((From )([0-9]+@[a-z]+)).*$"
    msg = ""

    for line in fp:
        res = re.search(regexp, line)

        if (res is None):
            msg += line.strip("\n")
        elif (res.group(2) == "From "):
            break

    return msg

''' 
    getMonthNum: Returns month number given name of month
'''
def getMonthNum(month):
    num = "0"

    if (month == "Jan"):
        num = "01"
    elif (month == "Feb"):
        num = "02"
    elif (month == "Mar"):
        num = "03"
    elif(month == "Apr"):
        num = "04"
    elif (month == "May"):
        num = "05"
    elif (month == "Jun"):
        num = "06"
    elif (month == "Jul"):
        num = "07"
    elif (month == "Aug"):
        num = "08"
    elif (month == "Sep"):
        num = "09"
    elif (month == "Oct"):
        num = "10"
    elif (month == "Nov"):
        num = "11"
    elif (month == "Dec"):
        num = "12"

    return num

'''
    getMMSStr: Extracts MMS message string from input file
'''
def getMMSStr(fp):
    # 30848
    fp.readline()
    fp.readline()

    endRegexp = "^(------([0-9A-Z]+).*)$"
    imgStr = ""

    for line in fp:
        res = re.search(endRegexp, line)
        if (res is None):
            imgStr += line.strip("\n")
        else:
            break

    return imgStr

'''
    decodeMMS: Creates image given base64 encoded string
'''
def decodeMMS(name, number, imgStr, ctr, contentType, dirPath): 
    imgName = getFullname(name) + str(number) + "_" + "img" + "_" + str(ctr)

    if (contentType == "image/jpeg"):
        imgName += ".jpg"
    elif (contentType == "image/png"):
        imgName += ".png"
    elif (contentType == "image/gif"):
        imgName += ".gif"

    imgPath = dirPath + "/" + imgName
    imgBytes = imgStr.encode('utf-8')
    #print(imgBytes)

    with open(imgPath, "wb") as fp: 
        imgData = base64.decodebytes(imgBytes)
        fp.write(imgData)

    return "Images/" + imgName

'''
    getFullname: Returns underscore-separated name string
'''
def getFullname(name):
    nameSplit = name.split(" ")
    fullname = ""
    for names in nameSplit:
        fullname += names + "_"

    return fullname

'''
    getHTML: generates HTML page for (up to) 1000 messages for given contact name and number
'''
def getHTML(name, number, msgList, filename):
    stylesheetName = "style.css"
    numberStr = str(number)
    docTitle = name + " at " + numberStr[0:2] + " " + numberStr[3:5] + " " + numberStr[6:9]

    doc = dominate.document(title=docTitle)
    with doc.head:
        tags.link(rel='stylesheet', href=stylesheetName)

    with doc:
        with tags.div(id='header').add(tags.ol()):
            for i in ['home', 'about', 'contract']:
                tags.li(tags.a(i.title()))
        
        with tags.div():
            tags.attr(cls='body')
            tags.p("wheeeee")

    with open(filename, "w") as fp:
        print(doc, file=fp)

def generateCSS():
    print("Generating 'style.css'")
    