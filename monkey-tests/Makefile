all: build
	pythonium -g > build/lib.js
	pythonium test.py > build/test.py.js
	cat build/lib.js build/test.py.js > build/exec.js
	nodejs --harmony build/exec.js

build:
	mkdir build

veloce:
	pythonium -V test.py > build/test.py.js
	nodejs --harmony build/test.py.js


