#!/usr/bin/env python3
import os
import sys
import difflib 
from traceback import print_exc
from subprocess import check_output, STDOUT, CalledProcessError

from pythonium.veloce import veloce_generate_js


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

    for test in os.listdir(TESTS_ROOT):
        if test.endswith('.py'):
            test_ctr += 1
            filepath = os.path.join(TESTS_ROOT, test)
            exec_script = os.path.join(TMPDIR, test + 'exec.js')
            with open(exec_script, 'w') as f:
                try:
                    veloce_generate_js(filepath, output=f)
                except Exception as exc:
                    print_exc()
                    print('< Translating {} failed with the above exception.'.format(test))
                    continue

            try:
                result = check_output(['nodejs', exec_script], stderr=STDOUT)
            except CalledProcessError as err:
                print(err.output.decode(errors='replace'))
                print('< {} ERROR :('.format(test))
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
                print('< {} FAILED :('.format(test))
            else:
                ok_ctr += 1
                print('< {} PASS :)'.format(test))

    print("= Passed {}/{} tests".format(ok_ctr, test_ctr))
