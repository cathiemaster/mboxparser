# -*- coding: utf-8 -*- 

# MBOX File Parser
# Catherine Master
# Started:
# Finished:

import glob, os, sys, shutil
import mbox

def getWorkingDir():
    mboxPath = input("Enter MBOX file path or press N to stay in current directory: ")

    if (mboxPath != "N"):
        cwd = os.getcwd()
        try:
            os.chdir(mboxPath)
        except:
            print("Specified path incorrect.")
            return False
    
    return True

def parse(fileList):
    filenames = glob.glob("*.mbox")

    for file in filenames: 
        fp = open(file, "r")
        (msgs, imgFileNames) = mbox.parseFile(fp, file)
        
        dirPath = input("Enter message directory path  or press N to stay in current directory: ")
        if (dirPath != "N"):
            try:
                os.chdir(dirPath)
            except:
                print("Unable to change directories to " + dirPath)

        print("Creating 'Messages' directory.")
        msgDir = os.getcwd() + "/Messages"
        if (os.path.isdir(msgDir) is False):
            try:
                os.mkdir("Messages")
            except:
                print("Unable to make 'Messages' directory at " + dirPath)

        print("Moving 'Images' directory.")
        curImgDir = os.getcwd() + "/Images"
        destImgDir = os.getcwd() + "/Messages/Images"

        if (os.path.isdir(curImgDir) is True):
            if (os.path.isdir(destImgDir) is False):
                shutil.move(curImgDir, destImgDir)
        else:
            print("'Images' directory does not exist. Exiting...")
            fp.close()
            break
        
        print("Begin processing messages for export...")
        try:
            os.chdir("Messages")
        except:
            print("Unable to access directory at: " + msgDir)

        mbox.writeToFile(msgs, imgFileNames, file)
        fp.close()

def main():
    res = getWorkingDir()
    if (res is False):
        print("Unable to start parsing. Exiting...")
    else:
        parse([])



if __name__ == "__main__":
    main()

    