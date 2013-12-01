build:
	mkdir build

compliant: build
	pythonium -g > build/lib.js
	pythonium pystone-pythonium-compliant.py > build/pystone-pythonium-compliant.py.js
	cat build/lib.js build/pystone-pythonium-compliant.py.js > build/exec-compliant.js
	time nodejs --harmony build/exec-compliant.js

veloce: build
	pythonium -V pystone-pythonium-veloce.py > build/pystone-pythonium-veloce.py.js
	cat classy.js build/pystone-pythonium-veloce.py.js > build/exec-veloce.js
	time nodejs --harmony build/exec-veloce.js

