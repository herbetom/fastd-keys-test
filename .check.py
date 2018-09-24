#!/usr/bin/env python3
from pathlib import Path
import re
import sys

exit_code = 0
key_pattern = re.compile('key\s*"(?P<key>[a-f0-9]{64})";');

ANSI_COLOR_ERR = "\x1b[31m"
ANSI_COLOR_WARN = "\x1b[33m"
ANSI_COLOR_OK = "\x1b[32m"
ANSI_COLOR_RESET = "\x1b[0m"

def error(*arg):
    print(ANSI_COLOR_ERR, *arg, file=sys.stderr,
          end='%s\n' % ANSI_COLOR_RESET)


def warn(*arg):
    print(ANSI_COLOR_WARN, *arg, file=sys.stderr,
          end='%s\n' % ANSI_COLOR_RESET)


def ok(*arg):
    print(ANSI_COLOR_OK, *arg, file=sys.stderr,
          end='%s\n' % ANSI_COLOR_RESET)


def key_from_file(fn):
    with open(fn, 'r', encoding='utf-8') as handle:
        for line in handle:
            line = line.strip()
            if line.startswith('#'):
                continue
            if line.lower().startswith('key'):
                return key_pattern.match(line)
    return False


keys = {}
root = Path('.')
for fn in root.iterdir():
    fn = str(fn)

    if fn.startswith('.'):
        continue

    data = key_from_file(fn)
    if not data:
        error('{fn}: has no (or no valid) key'.format(fn=fn))
        exit_code += 1
        continue

    keys.setdefault(data.group('key'), set()).add(fn)

for k, v in keys.items():
    if len(v) > 1:
        exit_code += 1
        error('duplicate key "{key}" in files: {files}'.format(
            key=k, files=', '.join(v)))

if exit_code > 0:
    error("{n} errors".format(n=exit_code))
else:
    ok("everything ok")
sys.exit(exit_code)

