__author__ = 'Jason'

import glob
import os
import fnmatch


class Mapper:
    #map out files{} -> classes{} -> functions{{inputs:[],returns:[]}
    #moduleMap = files{classes{functions{{inputs:[],returns:[]}}
    moduleMap = {"files":{}}
    RootJsfileList = []
    RootDir = os.curdir() #or js library folder path
    def __init__(self):
        pass
    def find_all_js_files(self,RootDir=RootDir):
        for root, dirnames, filenames in os.walk(RootDir):
            for filename in fnmatch.filter(filenames, '*.js'):
                self.moduleMap["files"] += {str(filename):""}
        pass

class Skelmaker:
    #Create Skeleton Python Modules For Easy Ide Intergration
    def __init__(self):
        pass
