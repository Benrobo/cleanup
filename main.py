# !/usr/

import sys
import os
import platform
import pathlib
import shutil
import getpass
from halo import Halo
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()

    
currDir = os.getcwd()
user = getpass.getuser()



info = """
    Cleanup

    -h, --help : list all commands available

    -rcd, --run-cd: clean up the directory from current directory where this script is been executed

    -p, --path (sys_path) [ /users/{username}/{directory} ] [optional:  (--move) ]: clean up directory from the path provided.
        By default, using the -p or --path command is set to (--copy)
"""

print("")

spinner = Halo(text='Cleaning up... \n\n', spinner='dots')


def copyFilesToDir(src, dest):
    shutil.copy(src, dest)
    return

def moveFilesToDir(src, dest):
    shutil.move(src, dest)
    return

def createFolders(store, commands):
    
    if len(store) > 0:
        spinner.start()
        for i, data in enumerate(store):
            folderPath = data["folderpath"]
            filePath = data["filePath"]
            fileName = data["fileName"]

            if not os.path.exists(folderPath):
                os.mkdir(folderPath)

            try:
                if os.path.exists(filePath) == True and os.path.isfile(filePath) == True:
                    
                    # check if the user added the --move command
                        
                    if "--move" in commands:
                        moveFilesToDir(filePath, folderPath)
                    else:
                        copyFilesToDir(filePath, folderPath)
                                    
                spinner.stop()
                print(colored(' Done cleaning up.. ', 'white', 'on_cyan'))
                    
            except:
                spinner.stop()
                print(colored(f" Destination path {folderPath}/{fileName} already exists ","white", "on_red"))

    


def parseArg():

    validCmd = ["-h", "--help", "-rcd", "--run-cd", "-p", "--path", "--copy", "--move"]
    arg = sys.argv
    result = {}
    
    # validate cmd
    if len(arg) > 1:
        if len(arg) < 3 and arg[1] == "-h" or arg[1] == "--help":
            result["error"] = False
            result["path"] = None
            result["info"] = info
            result["cmd"] = arg
            return result

        if len(arg) <= 3 and arg[1] == "-rcd" or arg[1] == "--run-cd":

            # return current directory
            result["error"] = False
            result["path"] = currDir
            result["info"] = None
            result["cmd"] = arg
            return result

        if len(arg) <= 4 and arg[1] == "-p" or arg[1] == "--path":
            # check the length of arg 
            try:
                path = arg[2]
                # check if path exists
                if os.path.exists(path) == False:
                    result["error"] = True
                    result["path"] = None
                    result["message"] = "path given doesnt exists"
                    result["info"] = None
                    result["cmd"] = arg
                    return result
                
                result["error"] = False
                result["path"] = path
                result["message"] = None
                result["info"] = None
                result["cmd"] = arg
                return result
                
            except:
                result["error"] = True
                result["path"] = path
                result["message"] = "Something went wrong parsing path"
                result["info"] = None
                result["cmd"] = arg
                return result
                
        result["error"] = True
        result["path"] = None
        result["message"] = "invalid command"
        result["info"] = None
        result["cmd"] = arg
        return result
    
    
                
def CleanUp():
    # for testing purpose
    # tempPath = "/users/benrobo/downloads/test-cleanup/"
    # files = os.listdir(tempPath)
    stores = []
    
    
    parseData = parseArg()
    commandsUsed = parseData["cmd"]
    
    if parseData["error"] == True:
        msg = parseData["message"]
        print(colored(f" {msg} ", "white", "on_red"))        
        return

    if parseData["error"] == False and parseData["info"] != None:
        data = parseData["info"]
        print(colored(data, "cyan"))        
        return

    if parseData["error"] == False and parseData["path"] != None:
        parsePath = parseData["path"]
        
        
        # check if files are available within that directory
        filesInDir = os.listdir(parsePath)
        countNonAvailableFiles = 0
        countAvailableFiles = 0
        
        for x in filesInDir:
            fileExt = pathlib.Path(x).suffix
            if fileExt == "" or fileExt == None:
                countNonAvailableFiles += 1
            
            elif fileExt != "" or fileExt != None:
                countAvailableFiles += 1
        
        if countNonAvailableFiles > countAvailableFiles:
            if countAvailableFiles == 0:
                print(colored(" Failed to cleanup directory: No file found within this directory. ", "white", "on_red"))
                return False
        
        for files in os.listdir(parsePath):
            fname = files
            fomatedFilename = files.split(".")
            
            
            if len(fomatedFilename) > 1:
                ext = pathlib.Path(fname).suffix.lstrip().replace(".","")

                if ext == "":
                    ext = fname.replace(".", "")
                
                if ext != ".git":
                    mediaStore = {
                        "folderpath": f"{parsePath}/{ext.upper()}",
                        "filePath": f"{parsePath}/{fname}",
                        "fileName": fname
                    }
                    
                    stores.append(mediaStore)
        createFolders(stores, commandsUsed)



if __name__ == "__main__":
    CleanUp() 
