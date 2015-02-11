__author__ = 'Jason'

import re
import os
import fnmatch


class Mapper:
    #map out files{} -> classes{} & Imports{} -> functions{{inputs:[],returns:[]}
    #moduleMap = files{{classes{functions{{inputs:[],returns:[]},"imports":[]}
    moduleMap = {"files":{}}
    RootJsfileList = []
    RootDir = os.curdir() #or js library folder path
    def __init__(self):
        pass
    def find_all_js_files(self,RootDir=RootDir):
        for root, dirnames, filenames in os.walk(RootDir):
            for filename in fnmatch.filter(filenames, '*.js'):
                self.moduleMap["files"] += {str(filename):""}
    def find_imports_in_file(self):
        imports = re.findall()
        return imports
    def find_all_classes_in_file(self):
        pass
    def find_all_functions_in_class(self):
        pass
    def get_inputs_from_function(self):
        pass
    def parseJSfile(self):
        pass


class Skelmaker:
    #Create Skeleton Python Modules For Easy Ide Intergration
    def __init__(self):
        pass
