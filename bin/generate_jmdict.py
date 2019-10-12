#!/usr/bin/env python3

import sys
import xml.etree.ElementTree

LANG_CONV = {
    'aar': 'aa', 'abk': 'ab', 'afr': 'af', 'aka': 'ak',
    'alb': 'sq', 'amh': 'am', 'ara': 'ar', 'arg': 'an',
    'arm': 'hy', 'asm': 'as', 'ava': 'av', 'ave': 'ae',
    'aym': 'ay', 'aze': 'az', 'bak': 'ba', 'bam': 'bm',
    'baq': 'eu', 'bel': 'be', 'ben': 'bn', 'bih': 'bh',
    'bis': 'bi', 'bos': 'bs', 'bre': 'br', 'bul': 'bg',
    'bur': 'my', 'cat': 'ca', 'cha': 'ch', 'che': 'ce',
    'chi': 'zh', 'chu': 'cu', 'chv': 'cv', 'cor': 'kw',
    'cos': 'co', 'cre': 'cr', 'cze': 'cs', 'dan': 'da',
    'div': 'dv', 'dut': 'nl', 'dzo': 'dz', 'eng': 'en',
    'epo': 'eo', 'est': 'et', 'ewe': 'ee', 'fao': 'fo',
    'fij': 'fj', 'fin': 'fi', 'fre': 'fr', 'fry': 'fy',
    'ful': 'ff', 'geo': 'ka', 'ger': 'de', 'gla': 'gd',
    'gle': 'ga', 'glg': 'gl', 'glv': 'gv', 'gre': 'el',
    'grn': 'gn', 'guj': 'gu', 'hat': 'ht', 'hau': 'ha',
    'heb': 'he', 'her': 'hz', 'hin': 'hi', 'hmo': 'ho',
    'hrv': 'hr', 'hun': 'hu', 'ibo': 'ig', 'ice': 'is',
    'ido': 'io', 'iii': 'ii', 'iku': 'iu', 'ile': 'ie',
    'ina': 'ia', 'ind': 'id', 'ipk': 'ik', 'ita': 'it',
    'jav': 'jv', 'jpn': 'ja', 'kal': 'kl', 'kan': 'kn',
    'kas': 'ks', 'kau': 'kr', 'kaz': 'kk', 'khm': 'km',
    'kik': 'ki', 'kin': 'rw', 'kir': 'ky', 'kom': 'kv',
    'kon': 'kg', 'kor': 'ko', 'kua': 'kj', 'kur': 'ku',
    'lao': 'lo', 'lat': 'la', 'lav': 'lv', 'lim': 'li',
    'lin': 'ln', 'lit': 'lt', 'ltz': 'lb', 'lub': 'lu',
    'lug': 'lg', 'mac': 'mk', 'mah': 'mh', 'mal': 'ml',
    'mao': 'mi', 'mar': 'mr', 'may': 'ms', 'mlg': 'mg',
    'mlt': 'mt', 'mon': 'mn', 'nau': 'na', 'nav': 'nv',
    'nbl': 'nr', 'nde': 'nd', 'ndo': 'ng', 'nep': 'ne',
    'nno': 'nn', 'nob': 'nb', 'nor': 'no', 'nya': 'ny',
    'oci': 'oc', 'oji': 'oj', 'ori': 'or', 'orm': 'om',
    'oss': 'os', 'pan': 'pa', 'per': 'fa', 'pli': 'pi',
    'pol': 'pl', 'por': 'pt', 'pus': 'ps', 'que': 'qu',
    'roh': 'rm', 'rum': 'ro', 'run': 'rn', 'rus': 'ru',
    'sag': 'sg', 'san': 'sa', 'sin': 'si', 'slo': 'sk',
    'slv': 'sl', 'sme': 'se', 'smo': 'sm', 'sna': 'sn',
    'snd': 'sd', 'som': 'so', 'sot': 'st', 'spa': 'es',
    'srd': 'sc', 'srp': 'sr', 'ssw': 'ss', 'sun': 'su',
    'swa': 'sw', 'swe': 'sv', 'tah': 'ty', 'tam': 'ta',
    'tat': 'tt', 'tel': 'te', 'tgk': 'tg', 'tgl': 'tl',
    'tha': 'th', 'tib': 'bo', 'tir': 'ti', 'ton': 'to',
    'tsn': 'tn', 'tso': 'ts', 'tuk': 'tk', 'tur': 'tr',
    'twi': 'tw', 'uig': 'ug', 'ukr': 'uk', 'urd': 'ur',
    'uzb': 'uz', 'ven': 've', 'vie': 'vi', 'vol': 'vo',
    'wel': 'cy', 'wln': 'wa', 'wol': 'wo', 'xho': 'xh',
    'yid': 'yi', 'yor': 'yo', 'zha': 'za', 'zul': 'zu',

    'mol': 'ro', 'chn': 'zh', 'scr': 'hr',  # Invalid codes
}

_DEFAULT = object()

def parse_list(elem, subelem_name):
    if elem is None:
        return []
    return [e.text for e in elem.findall(subelem_name)]

def parse_int(elem, subelem_name):
    if elem is None:
        return None
    sub = elem.find(subelem_name)
    if sub is not None:
        return int(sub.text)
    else:
        return None

def add_if_present(data, elem, subelem_name, value=_DEFAULT):
    subelems = elem.findall(subelem_name)
    if subelems:
        if value is _DEFAULT:
            if len(subelems) > 1:
                raise ValueError("Multiple {!r} elements found in {!r} element".format(subelem_name, elem.tag))
            value = subelems[0].text
        data[subelem_name] = value
    return data

def parse_k_ele(elem):
    data = {
        'keb': elem.find('keb').text,
        'ke_inf': parse_list(elem, 'ke_inf'),
        'ke_pri': parse_list(elem, 'ke_pri'),
    }
    return {k:v for k, v in data.items() if v}

def parse_r_ele(elem):
    data = {
        'reb': elem.find('reb').text,
        're_restr': parse_list(elem, 're_restr'),
        're_inf': parse_list(elem, 're_inf'),
        're_pri': parse_list(elem, 're_pri'),
    }
    add_if_present(data, elem, 're_nokanji', True)
    return {k:v for k, v in data.items() if v}

def parse_sense(elem, prev_sense):
    data = {
        'stagk': parse_list(elem, 'stagk'),
        'stagr': parse_list(elem, 'stagr'),
        'xref': parse_list(elem, 'xref'),
        'ant': parse_list(elem, 'ant'),
        'pos': parse_list(elem, 'pos'),
        'field': parse_list(elem, 'field'),
        'misc': parse_list(elem, 'misc'),
        'dial': parse_list(elem, 'dial'),
        'lsource': [parse_lsource(e) for e in elem.findall('lsource')],
        'gloss': parse_glosses(elem),
    }
    add_if_present(data, elem, 's_inf')
    if not data['pos']:
        data['pos'] = prev_sense.get('pos', [])
    if not data['misc']:
        data['misc'] = prev_sense.get('misc', [])
    return {k:v for k, v in data.items() if v}

def get_lang(elem):
    lang = elem.get('{http://www.w3.org/XML/1998/namespace}lang', 'eng')
    return LANG_CONV.get(lang, lang)

def parse_lsource(elem):
    data = {
        '': elem.text,
        'lang': get_lang(elem),
        'ls_type': elem.get('ls_type', 'full'),
        'ls_wasei': bool(elem.find('ls_wasei')),
    }
    return data

def parse_glosses(elem):
    data = {}
    for e in elem.findall('gloss'):
        lang = get_lang(e)
        gloss = {'': e.text}
        if e.get('g_gend'):
            gloss['g_gend'] = e.get('g_gend')
        if e.get('g_type'):
            gloss['g_type'] = e.get('g_type')
        data.setdefault(lang, []).append(gloss)
    return data

def parse_entry(elem):
    data = {
        'ent_seq': parse_int(elem, 'ent_seq'),
        'k_ele': [parse_k_ele(e) for e in elem.findall('k_ele')],
        'r_ele': [parse_r_ele(e) for e in elem.findall('r_ele')],
        'sense': [],
    }
    prev_sense = {}
    for e in elem.findall('sense'):
        s = parse_sense(e, prev_sense)
        data['sense'].append(s)
        prev_sense = s

def load_xml(filename):
    tree = xml.etree.ElementTree.parse(filename)
    root = tree.getroot()
    entries = [parse_entry(elem) for elem in root.iter('entry')]
    return entries

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


entries = load_xml(sys.argv[1])

sys.stdout.write('# -*- coding: utf-8 -*-\n')
sys.stdout.write('from __future__ import unicode_literals\n')
sys.stdout.write('\n')

sys.stdout.write('entries = ')
print_list(entries, '')
sys.stdout.write('\n')
