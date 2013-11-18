#!/usr/bin/env python3
import os
import sys
from difflib import Differ
from traceback import print_exc

from envoy import run

from pythonium_core import generate_js


ROOT = os.path.abspath(os.path.dirname(__file__))
TESTS_ROOT = os.path.join(ROOT, 'tests')


if __name__ == '__main__':
    for test in os.listdir(TESTS_ROOT):
        if test.endswith('.py'):
            filepath = os.path.join(TESTS_ROOT, test)
            exec_script = test + 'exec.js'
            exec_script = os.path.join('/tmp', exec_script)
            with open(exec_script, 'w') as f:
                try:
                    generate_js(filepath, output=f)
                except Exception as exc:
                    print_exc()
                    print('Translating {} failed with the above exception.'.format(test))
                    continue
            r = run('nodejs %s' % exec_script)
            if r.status_code != 0:
                print(r.std_out)
                print(r.std_err)
                print('%s ERROR :(' % test)
            else:
                r = run('python3 {}'.format(filepath))
                expected = r.std_out
                if r.status_code != 0:
                    print(r.std_out)
                    print(r.std_err)
                    print('%s PYTHON ERROR :(' % test)
                if expected == r.std_out:
                    print('%s PASS :)' % test)
                else:
                    compare = Differ().compare
                    diff = compare(expected.split('\n'), r.std_out.split('\n'))
                    for line in diff:
                        print(line)
                    print('%s FAILED :(' % test)
