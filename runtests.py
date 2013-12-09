#!/usr/bin/env python3
import os
import sys
import difflib 
from traceback import print_exc

from subprocess import PIPE
from subprocess import Popen
from subprocess import STDOUT
from subprocess import check_output
from subprocess import CalledProcessError


from pythonium.main import main
from pythonium.veloce.veloce import veloce_generate_js
from pythonium.compliant.compliant import compliant_generate_js


ROOT = os.path.abspath(os.path.dirname(__file__))
TESTS_ROOT = os.path.join(ROOT, 'tests')


def compare_output(expected, result):
    if isinstance(expected, bytes):
        expected = expected.decode(errors='replace')
    if isinstance(result, bytes):
        result = result.decode(errors='replace')
    expected = expected.strip().splitlines()
    result = result.strip().splitlines()
    diffs = difflib.unified_diff(expected, result, n=1, lineterm='',
                                 fromfile='expected', tofile='result')
    return list(diffs)


if __name__ == '__main__':
    ok_ctr = test_ctr = 0
    TMPDIR = os.path.join(TESTS_ROOT, 'tmp')
    try: os.mkdir(TMPDIR)
    except OSError: pass
    

    # XXX: this force to install pythonium before running tests
    COMPLIANTJS = Popen(["pythonium", "--generate"], stdout=PIPE).communicate()[0].decode('utf-8')

    for mode in ('veloce', 'compliant'):
        print('* Running tests for {} mode'.format(mode))
        for test in os.listdir(TESTS_ROOT):
            if test.endswith('.py'):
                print('< Running {} in {} mode.'.format(test, mode))
                # compliant mode must run any code even code written for veloce mode
                # but veloce mode can not run compliant tests
                if test.startswith('compliant-') and mode != 'compliant':
                    continue
                test_ctr += 1
                filepath = os.path.join(TESTS_ROOT, test)
                exec_script = os.path.join(TMPDIR, test + 'exec.js')
                with open(exec_script, 'w') as f:
                    try:
                        if mode =='veloce':
                            veloce_generate_js(filepath, output=f)
                        else:
                            f.write(COMPLIANTJS)
                            compliant_generate_js(filepath, output=f)
                    except Exception as exc:
                        print_exc()
                        print('< Translating {} in {} mode failed with the above exception.'.format(test, mode))
                        continue

                try:
                    result = check_output(['nodejs', exec_script], stderr=STDOUT)
                except CalledProcessError as err:
                    print(err.output.decode(errors='replace'))
                    print('< {} ERROR in {} mode :('.format(test, mode))
                    continue

                expected_file = os.path.join(TESTS_ROOT, test+'.expected')
                if os.path.exists(expected_file):
                    with open(expected_file, 'br') as f:
                        expected = f.read()
                else:
                    try:
                        expected = check_output(['python3', filepath], stderr=STDOUT)
                    except CalledProcessError as err:
                        print(err.output.decode(errors='replace'))
                        print('< {} PYTHON ERROR :('.format(test))
                        continue

                diffs = compare_output(expected, result)
                if diffs:
                    for line in diffs:
                        print(line)
                    print('< {} FAILED in {} mode :('.format(test, mode))
                else:
                    ok_ctr += 1
                    print('< {} PASS in {} mode :)'.format(test, mode))

    print("= Passed {}/{} tests".format(ok_ctr, test_ctr))
