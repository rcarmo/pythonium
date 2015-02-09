__author__ = 'Jason'

import glob
import os


class Mapper:
    #map out files -> classes -> functions+returns
    moduleMap = {}
    RootJsfileList = []
    def __init__(self):
        pass
    def _find_entry_Points(self):
        os.chdir("/mydir")
        for file in glob.glob("*.js"):
            print(file)
        pass

class Skelmaker:
    #Create Skeleton Python Modules For Easy Ide Intergration
    def __init__(self):
        pass
