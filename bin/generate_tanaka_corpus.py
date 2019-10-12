#!/usr/bin/env python3

import sys
import re

a_line_re = re.compile(r'A: (.*)\t(.*)#ID=([0-9_]*)')
b_word_re = re.compile(r'([^[({~]*)(\([^)]*\))?(\[[^]]*\])?({[^}]*})?(~)?$')

class FormatError (Exception):
    pass

def warn(text):
    sys.stderr.write('{}\n'.format(text))


def parse_a_line(text):
    m = a_line_re.match(text)
    if not m:
        raise FormatError('Could not parse "A:" line: {!r}'.format(text))
    return m.groups()

def trim_parens(text):
    if not text:
        return ''
    return text[1:-1]

def parse_b_line(text):
    words = text.split(' ')
    if words[0] != 'B:':
        raise FormatError('Could not parse "B:" line: {!r}'.format(text))
    results = []
    for word in words[1:]:
        m = b_word_re.match(word)
        if not m:
            raise FormatError('Could not parse word in "B:" line: {!r}'.format(word))
        info = list(m.groups())
        for i in range(1, 4):
            info[i] = trim_parens(info[i])
        info[2] = int(info[2] or 0)
        info[4] = bool(info[4])
        results.append((tuple(info[0:2]), info[2], info[3], info[4]))
    return results

def process_file(filename):
    data = []
    current_entry = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] == 'A':
                jp_text, en_text, id = parse_a_line(line)
                current_entry = {
                    'jp': jp_text,
                    'en': en_text,
                    'id': id,
                }
                data.append(current_entry)
            elif line[0] == 'B':
                if 'words' in current_entry:
                    warn('Duplicate "B:" line: {!r}'.format(line))
                    continue
                current_entry['words'] = parse_b_line(line)
            else:
                warn('Unrecognized line: {!r}'.format(line))
    return data

def print_dict(data, indent):
    if not data or (len(data) == 1 and not isinstance(list(data.values())[0], (dict, list))):
        sys.stdout.write(repr(data))
        return
    sys.stdout.write('{\n')
    for key, value in sorted(data.items()):
        sys.stdout.write('{}    {!r}: '.format(indent, key))
        if isinstance(value, dict):
            print_dict(value, indent + '    ')
        elif isinstance(value, list):
            print_list(value, indent + '    ')
        else:
            sys.stdout.write(repr(value))
        sys.stdout.write(',\n')
    sys.stdout.write(indent + '}')

def print_list(data, indent):
    if not data or (len(data) == 1 and not isinstance(data[0], (dict, list))):
        sys.stdout.write(repr(data))
        return
    sys.stdout.write('(\n')
    for value in data:
        sys.stdout.write('{}    '.format(indent))
        if isinstance(value, dict):
            print_dict(value, indent + '    ')
        elif isinstance(value, list):
            print_list(value, indent + '    ')
        else:
            sys.stdout.write(repr(value))
        sys.stdout.write(',\n')
    sys.stdout.write(indent + ')')


entries = process_file(sys.argv[1])

sys.stdout.write('# -*- coding: utf-8 -*-\n')
sys.stdout.write('from __future__ import unicode_literals\n')
sys.stdout.write('\n')

sys.stdout.write('entries = ')
print_list(entries, '')
sys.stdout.write('\n')
