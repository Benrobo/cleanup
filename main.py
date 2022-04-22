# !/usr/

import sys
import os
import platform
import pathlib
import shutil
import getpass
import time    
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

    -p, --path (sys_path) [ /users/{username}/{directory} ] : clean up directory from the path provided
"""

print("")

spinner = Halo(text='Cleaning up...', spinner='dots')

def createFolders(store):

    if len(store) > 0:
        spinner.start()
        for i, data in enumerate(store):
            folderPath = data["folderpath"]
            filePath = data["filePath"]
            
            if not os.path.exists(folderPath):
                os.mkdir(folderPath)

            if os.path.exists(filePath) == True:
                shutil.copy(filePath, folderPath)
        spinner.stop()
        print(colored(' Done cleaning up.. ', 'white', 'on_cyan'))
    


def parseArg():

    validCmd = ["-h", "--help", "-rcd", "--run-cd", "-p", "--path"]
    arg = sys.argv
    result = {}
    
    # validate cmd
    if len(arg) > 1:
        if len(arg) < 3 and arg[1] == "-h" or arg[1] == "--help":
            result["error"] = False
            result["path"] = None
            result["info"] = info
            return result

        if len(arg) <= 2 and arg[1] == "-rcd" or arg[1] == "--run-cd":

            # return current directory
            result["error"] = False
            result["path"] = currDir
            result["info"] = None
            return result

        if len(arg) == 3 and arg[1] == "-p" or arg[1] == "--path":
            # check the length of arg 
            try:
                path = arg[2]
                # check if path exists
                if os.path.exists(path) == False:
                    result["error"] = True
                    result["path"] = None
                    result["message"] = "path given doesnt exists"
                    result["info"] = None
                    return result
                
                result["error"] = False
                result["path"] = path
                result["message"] = None
                result["info"] = None
                return result
                
            except:
                result["error"] = True
                result["path"] = path
                result["message"] = "Something went wrong parsing path"
                result["info"] = None
                return result
                
        result["error"] = True
        result["path"] = None
        result["message"] = "invalid command"
        result["info"] = None
        return result
    
    
                
def CleanUp():
    # for testing purpose
    # tempPath = "/users/benrobo/downloads/test-rearrange/"
    # files = os.listdir(tempPath)
    stores = []
    
    
    parseData = parseArg()
    
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

        """
            If you wanna cleanup every files within an entire directory tree, uncomment this, and comment the below algorithmn
        """ 
        # for path, dirs, files in os.walk(parsePath):

        #     for i, fname in enumerate(files):
                
        #         ext = pathlib.Path(fname).suffix.lstrip().replace(".","")
        #         mediaStore = {
        #             "folderpath": f"{parsePath}/{ext.upper()}",
        #             "filePath": f"{parsePath}/{fname}"
        #         }
            
        #         stores.append(mediaStore)
    
        # createFolders(stores)
        
        for files in os.listdir(parsePath):
            # for i, fname in enumerate(files):
            fname = files
            fomatedFilename = files.split(".")
            
            if len(fomatedFilename) > 1:
                ext = pathlib.Path(fname).suffix.lstrip().replace(".","")
                mediaStore = {
                    "folderpath": f"{parsePath}/{ext.upper()}",
                    "filePath": f"{parsePath}/{fname}"
                }
        
                stores.append(mediaStore)
        createFolders(stores)



if __name__ == "__main__":
    CleanUp() 
