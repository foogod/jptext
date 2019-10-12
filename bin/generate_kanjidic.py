#!/usr/bin/env python3

import sys
import xml.etree.ElementTree

def parse_list(elem, subelem_name):
    if elem is None:
        return []
    return [e.text for e in elem.findall(subelem_name)]

def parse_elem(elem, dont_include=[]):
    value = dict(elem.attrib)
    for k in dont_include:
        try:
            del value[k]
        except KeyError:
            pass
    value[''] = elem.text
    return value

def parse_dict(elem, subelem_name, key_attr, default_key=None):
    if elem is None:
        return {}
    return {e.get(key_attr, default_key): e.text for e in elem.findall(subelem_name)}

def parse_dict_with_attrs(elem, subelem_name, key_attr, default_key=None):
    if elem is None:
        return {}
    return {e.get(key_attr, default_key): parse_elem(e, [key_attr]) for e in elem.findall(subelem_name)}

def parse_multidict(elem, subelem_name, key_attr, default_key=None):
    if elem is None:
        return {}
    result = {}
    for e in elem.findall(subelem_name):
        key = e.get(key_attr, default_key)
        result.setdefault(key, []).append(e.text)
    return result

def parse_multidict_with_attrs(elem, subelem_name, key_attr, default_key=None):
    if elem is None:
        return {}
    result = {}
    for e in elem.findall(subelem_name):
        key = e.get(key_attr, default_key)
        result.setdefault(key, []).append(parse_elem(e, [key_attr]))
    return result

def parse_int(elem, subelem_name):
    if elem is None:
        return None
    sub = elem.find(subelem_name)
    if sub is not None:
        return int(sub.text)
    else:
        return None

def parse_misc(elem):
    return {
        'grade': parse_int(elem, 'grade'),
        'stroke_count': parse_int(elem, 'stroke_count'),
        'variant': parse_dict(elem, 'variant', 'var_type'),
        'freq': parse_int(elem, 'freq'),
        'jlpt': parse_int(elem, 'jlpt'),
        'rad_name': parse_list(elem, 'rad_name'),
    }

def parse_reading_meaning(elem):
    results = {
        'rmgroup': [],
        'nanori': parse_list(elem, 'nanori'),
    }
    if elem is None:
        return results
    for rmgroup in elem.findall('rmgroup'):
        data = {}
        data['reading'] = parse_multidict_with_attrs(rmgroup, 'reading', 'r_type')
        data['meaning'] = parse_multidict(rmgroup, 'meaning', 'm_lang', 'en')
        results['rmgroup'].append(data)
    return results

def load_xml(filename):
    tree = xml.etree.ElementTree.parse(filename)
    root = tree.getroot()
    elem = root.find('header')
    header = {
        'file_version': elem.find('file_version').text,
        'database_version': elem.find('database_version').text,
        'date_of_creation': elem.find('date_of_creation').text,
    }
    characters = []
    for elem in root.iter('character'):
        data = {
            'literal': elem.find('literal').text,
            'codepoint': parse_dict(elem.find('codepoint'), 'cp_value', 'cp_type'),
            'radical': parse_dict(elem.find('radical'), 'rad_value', 'rad_type'),
            'misc': parse_misc(elem.find('misc')),
            'dic_number': parse_dict_with_attrs(elem.find('dic_number'), 'dic_ref', 'dr_type'),
            'query_code': parse_dict_with_attrs(elem.find('query_code'), 'q_code', 'qc_type'),
            'reading_meaning': parse_reading_meaning(elem.find('reading_meaning')),
        }
        characters.append(data)
    return (header, characters)

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
    sys.stdout.write('[\n')
    for value in data:
        sys.stdout.write('{}    '.format(indent))
        if isinstance(value, dict):
            print_dict(value, indent + '    ')
        elif isinstance(value, list):
            print_list(value, indent + '    ')
        else:
            sys.stdout.write(repr(value))
        sys.stdout.write(',\n')
    sys.stdout.write(indent + ']')


header, characters = load_xml(sys.argv[1])

sys.stdout.write('# -*- coding: utf-8 -*-\n')
sys.stdout.write('from __future__ import unicode_literals\n')
sys.stdout.write('\n')

sys.stdout.write('header = ')
print_dict(header, '')
sys.stdout.write('\n\n')

sys.stdout.write('characters = ')
print_list(characters, '')
sys.stdout.write('\n')
