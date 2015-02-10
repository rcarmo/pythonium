__author__ = 'Jason'

from pythonium.BowerLoad import JsLibraryAnalyser
import setuptools_bower

class BowerLoader:
    def __init__(self):
        if not bower.BowerAdapter.is_bower_exists():
            print("please install bower from the system terminal/command prompt with 'npm install bower")
            raise Exception("Bower Is Not Installed or Accessable from the system console Path")
        bower = setuptools_bower()

    def createLibrarySkeletons(self,PackageName):
        LibraryMap = JsLibraryAnalyser
        return LibraryMap

    def load(self,PackageName):
        self.createLibrarySkeletons(PackageName)
        pass