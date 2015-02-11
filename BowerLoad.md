#Bower Load#

this is a helper module for pythonium to help with your ide autocompletes and help you explore a bower loaded javascript package.

it does this by downloading the bower package and and constructing a python package skeleton from the downloaded and analysed javascript.


### example ###

from pythonium.BowerLoad import loader as bower 
                                      
fancyjsscript = bower.load("some-javascript-package") 

output = fancyjsscript.javascriptlibrary.javascriptclass.javascriptfunction("pickles-etc") 

print(output)

### meaning? ###

that javascript can be coded entirely without looking at any .js files!

python will be able to hijack any javascript module!

## Status ##

pre-alpha. the rest of the pythonium module works fine.

this so far is definitely a work in progress. im currently looking for work contributions, so please fork and push :D


## Requirements ##

setuptools_bower is currently required for this portion of the module

pip install setuptools_bower


## TODO ##

find or make a module that will build a python module skeleton from a predifined structure that is described in a dict or string. (ideas welcome)

## Contact for this portion of the build ##

https://groups.google.com/forum/#!forum/pythonium-users

### initial developer ###

twitter: @deddokatana

github: deddokatana