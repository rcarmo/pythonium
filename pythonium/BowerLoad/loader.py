__author__ = 'Jason'

from pythonium.BowerLoad import bower,JsLibraryAnalyser

class BowerLoader:
    def __init__(self):
        if not bower.BowerAdapter.is_bower_exists():
            print("please install bower from the system terminal/command prompt with 'npm install bower")
            raise Exception("Bower Is Not Installed or Accessable from the system console Path")

    def createLibrarySkeletons(self,PackageName):
        LibraryMap = JsLibraryAnalyser
        return LibraryMap

    def load(self,PackageName):
        bower.install(PackageName)
        self.createLibrarySkeletons(PackageName)
        pass