#!/usr/bin/env python3

import sys
import xml.etree.ElementTree

# fmt: off
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

ENTITIES = {
    "MA": "martial arts term",
    "X": "rude or X-rated term (not displayed in educational software)",
    "abbr": "abbreviation",
    "adj-i": "adjective (keiyoushi)",
    "adj-ix": "adjective (keiyoushi) - yoi/ii class",
    "adj-na": "adjectival nouns or quasi-adjectives (keiyodoshi)",
    "adj-no": "nouns which may take the genitive case particle `no'",
    "adj-pn": "pre-noun adjectival (rentaishi)",
    "adj-t": "`taru' adjective",
    "adj-f": "noun or verb acting prenominally",
    "adv": "adverb (fukushi)",
    "adv-to": "adverb taking the `to' particle",
    "arch": "archaism",
    "ateji": "ateji (phonetic) reading",
    "aux": "auxiliary",
    "aux-v": "auxiliary verb",
    "aux-adj": "auxiliary adjective",
    "Buddh": "Buddhist term",
    "chem": "chemistry term",
    "chn": "children's language",
    "col": "colloquialism",
    "comp": "computer terminology",
    "conj": "conjunction",
    "cop-da": "copula",
    "ctr": "counter",
    "derog": "derogatory",
    "eK": "exclusively kanji",
    "ek": "exclusively kana",
    "exp": "expressions (phrases, clauses, etc.)",
    "fam": "familiar language",
    "fem": "female term or language",
    "food": "food term",
    "geom": "geometry term",
    "gikun": "gikun (meaning as reading) or jukujikun (special kanji reading)",
    "hon": "honorific or respectful (sonkeigo) language",
    "hum": "humble (kenjougo) language",
    "iK": "word containing irregular kanji usage",
    "id": "idiomatic expression",
    "ik": "word containing irregular kana usage",
    "int": "interjection (kandoushi)",
    "io": "irregular okurigana usage",
    "iv": "irregular verb",
    "ling": "linguistics terminology",
    "m-sl": "manga slang",
    "male": "male term or language",
    "male-sl": "male slang",
    "math": "mathematics",
    "mil": "military",
    "n": "noun (common) (futsuumeishi)",
    "n-adv": "adverbial noun (fukushitekimeishi)",
    "n-suf": "noun, used as a suffix",
    "n-pref": "noun, used as a prefix",
    "n-t": "noun (temporal) (jisoumeishi)",
    "num": "numeric",
    "oK": "word containing out-dated kanji",
    "obs": "obsolete term",
    "obsc": "obscure term",
    "ok": "out-dated or obsolete kana usage",
    "oik": "old or irregular kana form",
    "on-mim": "onomatopoeic or mimetic word",
    "pn": "pronoun",
    "poet": "poetical term",
    "pol": "polite (teineigo) language",
    "pref": "prefix",
    "proverb": "proverb",
    "prt": "particle",
    "physics": "physics terminology",
    "quote": "quotation",
    "rare": "rare",
    "sens": "sensitive",
    "sl": "slang",
    "suf": "suffix",
    "uK": "word usually written using kanji alone",
    "uk": "word usually written using kana alone",
    "unc": "unclassified",
    "yoji": "yojijukugo",
    "v1": "Ichidan verb",
    "v1-s": "Ichidan verb - kureru special class",
    "v2a-s": "Nidan verb with 'u' ending (archaic)",
    "v4h": "Yodan verb with `hu/fu' ending (archaic)",
    "v4r": "Yodan verb with `ru' ending (archaic)",
    "v5aru": "Godan verb - -aru special class",
    "v5b": "Godan verb with `bu' ending",
    "v5g": "Godan verb with `gu' ending",
    "v5k": "Godan verb with `ku' ending",
    "v5k-s": "Godan verb - Iku/Yuku special class",
    "v5m": "Godan verb with `mu' ending",
    "v5n": "Godan verb with `nu' ending",
    "v5r": "Godan verb with `ru' ending",
    "v5r-i": "Godan verb with `ru' ending (irregular verb)",
    "v5s": "Godan verb with `su' ending",
    "v5t": "Godan verb with `tsu' ending",
    "v5u": "Godan verb with `u' ending",
    "v5u-s": "Godan verb with `u' ending (special class)",
    "v5uru": "Godan verb - Uru old class verb (old form of Eru)",
    "vz": "Ichidan verb - zuru verb (alternative form of -jiru verbs)",
    "vi": "intransitive verb",
    "vk": "Kuru verb - special class",
    "vn": "irregular nu verb",
    "vr": "irregular ru verb, plain form ends with -ri",
    "vs": "noun or participle which takes the aux. verb suru",
    "vs-c": "su verb - precursor to the modern suru",
    "vs-s": "suru verb - special class",
    "vs-i": "suru verb - included",
    "kyb": "Kyoto-ben",
    "osb": "Osaka-ben",
    "ksb": "Kansai-ben",
    "ktb": "Kantou-ben",
    "tsb": "Tosa-ben",
    "thb": "Touhoku-ben",
    "tsug": "Tsugaru-ben",
    "kyu": "Kyuushuu-ben",
    "rkb": "Ryuukyuu-ben",
    "nab": "Nagano-ben",
    "hob": "Hokkaido-ben",
    "vt": "transitive verb",
    "vulg": "vulgar expression or word",
    "adj-kari": "`kari' adjective (archaic)",
    "adj-ku": "`ku' adjective (archaic)",
    "adj-shiku": "`shiku' adjective (archaic)",
    "adj-nari": "archaic/formal form of na-adjective",
    "n-pr": "proper noun",
    "v-unspec": "verb unspecified",
    "v4k": "Yodan verb with `ku' ending (archaic)",
    "v4g": "Yodan verb with `gu' ending (archaic)",
    "v4s": "Yodan verb with `su' ending (archaic)",
    "v4t": "Yodan verb with `tsu' ending (archaic)",
    "v4n": "Yodan verb with `nu' ending (archaic)",
    "v4b": "Yodan verb with `bu' ending (archaic)",
    "v4m": "Yodan verb with `mu' ending (archaic)",
    "v2k-k": "Nidan verb (upper class) with `ku' ending (archaic)",
    "v2g-k": "Nidan verb (upper class) with `gu' ending (archaic)",
    "v2t-k": "Nidan verb (upper class) with `tsu' ending (archaic)",
    "v2d-k": "Nidan verb (upper class) with `dzu' ending (archaic)",
    "v2h-k": "Nidan verb (upper class) with `hu/fu' ending (archaic)",
    "v2b-k": "Nidan verb (upper class) with `bu' ending (archaic)",
    "v2m-k": "Nidan verb (upper class) with `mu' ending (archaic)",
    "v2y-k": "Nidan verb (upper class) with `yu' ending (archaic)",
    "v2r-k": "Nidan verb (upper class) with `ru' ending (archaic)",
    "v2k-s": "Nidan verb (lower class) with `ku' ending (archaic)",
    "v2g-s": "Nidan verb (lower class) with `gu' ending (archaic)",
    "v2s-s": "Nidan verb (lower class) with `su' ending (archaic)",
    "v2z-s": "Nidan verb (lower class) with `zu' ending (archaic)",
    "v2t-s": "Nidan verb (lower class) with `tsu' ending (archaic)",
    "v2d-s": "Nidan verb (lower class) with `dzu' ending (archaic)",
    "v2n-s": "Nidan verb (lower class) with `nu' ending (archaic)",
    "v2h-s": "Nidan verb (lower class) with `hu/fu' ending (archaic)",
    "v2b-s": "Nidan verb (lower class) with `bu' ending (archaic)",
    "v2m-s": "Nidan verb (lower class) with `mu' ending (archaic)",
    "v2y-s": "Nidan verb (lower class) with `yu' ending (archaic)",
    "v2r-s": "Nidan verb (lower class) with `ru' ending (archaic)",
    "v2w-s": "Nidan verb (lower class) with `u' ending and `we' conjugation (archaic)",
    "archit": "architecture term",
    "astron": "astronomy, etc. term",
    "baseb": "baseball term",
    "biol": "biology term",
    "bot": "botany term",
    "bus": "business term",
    "econ": "economics term",
    "engr": "engineering term",
    "finc": "finance term",
    "geol": "geology, etc. term",
    "law": "law, etc. term",
    "mahj": "mahjong term",
    "med": "medicine, etc. term",
    "music": "music term",
    "Shinto": "Shinto term",
    "shogi": "shogi term",
    "sports": "sports term",
    "sumo": "sumo term",
    "zool": "zoology term",
    "joc": "jocular, humorous term",
    "anat": "anatomical term",
}

ENTITY_LOOKUP = {v: k for k, v in ENTITIES.items()}

POS_SIMPLE = {
    'adj-f': 'adjective (pre-noun)',
    'adj-i': 'い-adjective',
    'adj-ix': 'い-adjective',
    'adj-ku': 'く-adjective',
    'adj-na': 'な-adjective',
    'adj-nari': 'な-adjective (formal/archaic)',
    'adj-no': 'の-adjective',
    'adj-pn': 'adjective (pre-noun)',
    'adj-ku': 'しく-adjective',
    'adj-t': 'たる-adjective',
    'adv': 'adverb',
    'adv-to': 'と-adverb',
    'exp': 'expression',
    'int': 'interjection',
    'n': 'noun',
    'n-adv': 'adverbial noun',
    'n-pref': 'noun (prefix)',
    'n-suf': 'noun (suffix)',
    'n-t': 'noun (temporal)',
    'v-unspec': 'verb',
    'v1': 'ichidan verb',
    'v1-s': 'ichidan verb',
    'v2a-s': 'nidan verb',
    'v2b-k': 'nidan verb',
    'v2b-s': 'nidan verb',
    'v2d-k': 'nidan verb',
    'v2d-s': 'nidan verb',
    'v2g-k': 'nidan verb',
    'v2g-s': 'nidan verb',
    'v2h-k': 'nidan verb',
    'v2h-s': 'nidan verb',
    'v2k-k': 'nidan verb',
    'v2k-s': 'nidan verb',
    'v2m-k': 'nidan verb',
    'v2m-s': 'nidan verb',
    'v2n-s': 'nidan verb',
    'v2r-k': 'nidan verb',
    'v2r-s': 'nidan verb',
    'v2s-s': 'nidan verb',
    'v2t-k': 'nidan verb',
    'v2t-s': 'nidan verb',
    'v2w-s': 'nidan verb',
    'v2y-k': 'nidan verb',
    'v2y-s': 'nidan verb',
    'v2z-s': 'nidan verb',
    'v4b': 'yodan verb',
    'v4g': 'yodan verb',
    'v4h': 'yodan verb',
    'v4k': 'yodan verb',
    'v4m': 'yodan verb',
    'v4n': 'yodan verb',
    'v4r': 'yodan verb',
    'v4s': 'yodan verb',
    'v4t': 'yodan verb',
    'v5aru': 'godan verb',
    'v5b': 'godan verb',
    'v5g': 'godan verb',
    'v5k': 'godan verb',
    'v5k-s': 'godan verb (special)',
    'v5m': 'godan verb',
    'v5n': 'godan verb',
    'v5r': 'godan verb',
    'v5r-i': 'irregular verb',
    'v5s': 'godan verb',
    'v5t': 'godan verb',
    'v5u': 'godan verb',
    'v5u-s': 'godan verb',
    'v5uru': 'godan verb',
    'vk': 'kuru verb',
    'vn': 'godan verb',
    'vr': 'irregular verb',
    'vs': 'する-noun',
    'vs-i': 'suru verb',
    'vs-s': 'suru verb',
    'vz': 'ichidan verb',
}

POS_DETAILS = {
    'adj-f':    ('adj',  'pre-noun'),
    'adj-i':    ('adj',  'i'),
    'adj-ix':   ('adj',  'i'),
    'adj-ku':   ('adj',  'ku'),
    'adj-na':   ('adj',  'na'),
    'adj-nari': ('adj',  'nari'),
    'adj-no':   ('adj',  'no'),
    'adj-pn':   ('adj',  'pre-noun',),
    'adj-shiku': ('adj', 'shiku'),
    'adj-t':    ('adj',  'taru'),
    'adv':      ('adv',  None),
    'adv-to':   ('adv',  'to'),
    'aux':      ('aux',  None),
    'conj':     ('conj', None),
    'cop-da':   ('verb', 'copula'),
    'ctr':      ('counter', None),
    'exp':      ('expr', None),
    'int':      ('int',  None),
    'n':        ('noun', None),
    'n-adv':    ('noun', 'adv'),
    'n-pr':     ('noun', 'proper'),
    'n-pref':   ('noun', 'prefix'),
    'n-suf':    ('noun', 'suffix'),
    'n-t':      ('noun', 'temporal'),
    'num':      ('numeric', None),
    'pref':     ('prefix', None),
    'prt':      ('particle', None),
    'pn':       ('pronoun', None),
    'suf':      ('suffix', None),
    'unc':      (None, None),
    'v-unspec': ('verb', None),
    'v1':       ('verb', 'ichidan'),
    'v1-s':     ('verb', 'ichidan'),
    'v2a-s':    ('verb', 'nidan'),
    'v2b-k':    ('verb', 'nidan'),
    'v2b-s':    ('verb', 'nidan'),
    'v2d-k':    ('verb', 'nidan'),
    'v2d-s':    ('verb', 'nidan'),
    'v2g-k':    ('verb', 'nidan'),
    'v2g-s':    ('verb', 'nidan'),
    'v2h-k':    ('verb', 'nidan'),
    'v2h-s':    ('verb', 'nidan'),
    'v2k-k':    ('verb', 'nidan'),
    'v2k-s':    ('verb', 'nidan'),
    'v2m-k':    ('verb', 'nidan'),
    'v2m-s':    ('verb', 'nidan'),
    'v2n-s':    ('verb', 'nidan'),
    'v2r-k':    ('verb', 'nidan'),
    'v2r-s':    ('verb', 'nidan'),
    'v2s-s':    ('verb', 'nidan'),
    'v2t-k':    ('verb', 'nidan'),
    'v2t-s':    ('verb', 'nidan'),
    'v2w-s':    ('verb', 'nidan'),
    'v2y-k':    ('verb', 'nidan'),
    'v2y-s':    ('verb', 'nidan'),
    'v2z-s':    ('verb', 'nidan'),
    'v4b':      ('verb', 'yodan'),
    'v4g':      ('verb', 'yodan'),
    'v4h':      ('verb', 'yodan'),
    'v4k':      ('verb', 'yodan'),
    'v4m':      ('verb', 'yodan'),
    'v4n':      ('verb', 'yodan'),
    'v4r':      ('verb', 'yodan'),
    'v4s':      ('verb', 'yodan'),
    'v4t':      ('verb', 'yodan'),
    'v5aru':    ('verb', 'godan'),
    'v5b':      ('verb', 'godan'),
    'v5g':      ('verb', 'godan'),
    'v5k':      ('verb', 'godan'),
    'v5k-s':    ('verb', 'irregular'),
    'v5m':      ('verb', 'godan'),
    'v5n':      ('verb', 'godan'),
    'v5r':      ('verb', 'godan'),
    'v5r-i':    ('verb', 'irregular'),
    'v5s':      ('verb', 'godan'),
    'v5t':      ('verb', 'godan'),
    'v5u':      ('verb', 'godan'),
    'v5u-s':    ('verb', 'godan'),
    'v5uru':    ('verb', 'godan'),
    'vk':       ('verb', 'kuru'),
    'vn':       ('verb', 'godan'),
    'vr':       ('verb', 'irregular'), #FIXME: archaic
    'vs':       ('noun', 'suru'),
    'vs-i':     ('verb', 'suru'),
    'vs-s':     ('verb', 'suru'),
    'vz':       ('verb', 'ichidan'),
}

MISC_ATTRS = {
    'abbr': 'abbr',
    'arch': 'archaism',
    'chn': 'childrens_language',
    'col': 'colloquialism',
    'derog': 'derogatory',
    'fam': 'familiar_language',
    'fem': 'female_language',
    'hon': 'honorific',
    'hum': 'humble',
    'id': 'idiomatic',
    'joc': 'jocular_language',
    'm-sl': 'manga_slang',
    'male': 'male_language',
    'obs': 'obsolete',
    'obsc': 'obscure',
    'on-mim': 'onomatopoeic',
    'poet': 'poetical',
    'pol': 'polite_language',
    'proverb': 'proverb',
    'quote': 'quote',
    'rare': 'rare',
    'sens': 'sensitive',
    'sl': 'slang',
    'uk': 'usually_kana',
    'vulg': 'vulgar_language',
    'yoji': 'yojijukugo',
}
# fmt: on

_DEFAULT = object()


def warn(msg):
    sys.stderr.write("WARNING: {}\n".format(msg))


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
    data = {"keb": elem.find("keb").text, "ke_inf": parse_list(elem, "ke_inf"), "ke_pri": parse_list(elem, "ke_pri")}
    return {k: v for k, v in data.items() if v}


def parse_r_ele(elem):
    data = {
        "reb": elem.find("reb").text,
        "re_restr": parse_list(elem, "re_restr"),
        "re_inf": parse_list(elem, "re_inf"),
        "re_pri": parse_list(elem, "re_pri"),
    }
    add_if_present(data, elem, "re_nokanji", True)
    return {k: v for k, v in data.items() if v}


def parse_sense(elem, prev_sense):
    data = {
        "stagk": parse_list(elem, "stagk"),
        "stagr": parse_list(elem, "stagr"),
        "xref": parse_list(elem, "xref"),
        "ant": parse_list(elem, "ant"),
        "pos": parse_list(elem, "pos"),
        "field": parse_list(elem, "field"),
        "misc": parse_list(elem, "misc"),
        "dial": parse_list(elem, "dial"),
        "lsource": [parse_lsource(e) for e in elem.findall("lsource")],
        "gloss": parse_glosses(elem),
    }
    add_if_present(data, elem, "s_inf")
    data['pos'] = [ENTITY_LOOKUP[p] for p in data['pos']]
    data['misc'] = [ENTITY_LOOKUP[m] for m in data['misc']]
    return {k: v for k, v in data.items() if v}


def get_lang(elem):
    lang = elem.get("{http://www.w3.org/XML/1998/namespace}lang", "eng")
    return LANG_CONV.get(lang, lang)


def parse_lsource(elem):
    data = {
        "": elem.text,
        "lang": get_lang(elem),
        "ls_type": elem.get("ls_type", "full"),
        "ls_wasei": bool(elem.find("ls_wasei")),
    }
    return data


def parse_glosses(elem):
    data = {}
    for e in elem.findall("gloss"):
        lang = get_lang(e)
        gloss = {"": e.text}
        if e.get("g_gend"):
            gloss["g_gend"] = e.get("g_gend")
        if e.get("g_type"):
            gloss["g_type"] = e.get("g_type")
        data.setdefault(lang, []).append(gloss)
    return data


def parse_entry(elem):
    data = {
        "ent_seq": parse_int(elem, "ent_seq"),
        "k_ele": [parse_k_ele(e) for e in elem.findall("k_ele")],
        "r_ele": [parse_r_ele(e) for e in elem.findall("r_ele")],
        "sense": [],
    }
    prev_sense = {}
    for e in elem.findall("sense"):
        if not e:
            continue
        s = parse_sense(e, prev_sense)
        data["sense"].append(s)
        prev_sense = s
    return data


def load_xml(filename):
    tree = xml.etree.ElementTree.parse(filename)
    root = tree.getroot()
    entries = [parse_entry(elem) for elem in root.iter("entry")]
    return entries


def print_dict(data, indent):
    if not data or (len(data) == 1 and not isinstance(list(data.values())[0], (dict, list))):
        sys.stdout.write(repr(data))
        return
    sys.stdout.write("{\n")
    for key, value in sorted(data.items()):
        sys.stdout.write("{}    {!r}: ".format(indent, key))
        if isinstance(value, dict):
            print_dict(value, indent + "    ")
        elif isinstance(value, list):
            print_list(value, indent + "    ")
        else:
            sys.stdout.write(repr(value))
        sys.stdout.write(",\n")
    sys.stdout.write(indent + "}")


def print_list(data, indent):
    if not data or (len(data) == 1 and not isinstance(data[0], (dict, list))):
        sys.stdout.write(repr(data))
        return
    sys.stdout.write("[\n")
    for value in data:
        sys.stdout.write("{}    ".format(indent))
        if isinstance(value, dict):
            print_dict(value, indent + "    ")
        elif isinstance(value, list):
            print_list(value, indent + "    ")
        else:
            sys.stdout.write(repr(value))
        sys.stdout.write(",\n")
    sys.stdout.write(indent + "]")


def senses_overlap(sense, prev_sense):
    for field in ["stagk", "stagr", "xref", "ant", "pos", "field", "misc", "dial", "lsource", "s_inf"]:
        if field in sense and prev_sense.get(field) != sense[field]:
            return False
    for lang in sense["gloss"].keys():
        if lang in prev_sense["gloss"]:
            return False
    return True


def pos_details(pos):
    result = []
    vt = 'vt' in pos
    vi = 'vi' in pos
    vsc = 'vs-c' in pos
    auxv = 'aux-v' in pos
    auxa = 'aux-adj' in pos
    seen = set()
    verb_subcats = set()
    if vsc and 'v5s' not in pos:
        # Some entries have 'vs-c', but not 'v5s', but all vs-c verbs should also be v5s verbs.
        pos.append('v5s')
    for p in pos:
        if p in seen:
            continue
        seen.add(p)
        if p not in POS_DETAILS:
            continue
        full_desc = ENTITIES[p]
        simple_desc = POS_SIMPLE.get(p, full_desc)
        cat, subcat = POS_DETAILS[p]
        archaic = '(archaic)' in full_desc
        pd = {'tag': p, 'full_desc': full_desc, 'simple_desc': simple_desc, 'cat': cat, 'subcat': subcat, 'archaic': archaic}
        if cat == 'verb':
            pd['transitive'] = vt
            pd['intransitive'] = vi
            pd['auxiliary'] = auxv
            pd['su_verb'] = vsc
            verb_subcats.add(subcat)
        if cat == 'adj':
            pd['auxiliary'] = auxa
        result.append(pd)
    if len(verb_subcats) > 1:
        if 'irregular' in verb_subcats:
            result = [pd for pd in result if pd['cat'] != 'verb' or pd['subcat'] == 'irregular']
        else:
            warn("Conflicting verb types in same pos: {!r}".format(tuple(verb_subcats)))
    return result


def postprocess(entries):
    for entry in entries:
        senses = []
        for sense in entry['sense']:
            found = False
            for prev_sense in senses:
                if senses_overlap(sense, prev_sense):
                    # There is nothing different from a previous sense, except a
                    # definition in a different language than before.  Consider these
                    # to be the same sense with multiple languages instead (the way it
                    # should have been to begin with).
                    prev_sense['gloss'].update(sense['gloss'])
                    found = True
                    break
            if not found:
                senses.append(sense)

        prev_sense = senses[0]
        for sense in senses:
            if sense.get("pos"):
                sense['pos_details'] = pos_details(sense['pos'])
            else:
                sense["pos"] = prev_sense.get("pos", [])
                sense["pos_details"] = prev_sense.get("pos_details", [])
            if not sense.get('misc'):
                sense["misc"] = prev_sense.get("misc", [])
            for k, v in MISC_ATTRS.items():
                if k in sense['misc']:
                    sense[v] = True
            prev_sense = sense
        entry['sense'] = senses


entries = load_xml(sys.argv[1])
postprocess(entries)

sys.stdout.write("# -*- coding: utf-8 -*-\n")
sys.stdout.write("from __future__ import unicode_literals\n")
sys.stdout.write("\n")

sys.stdout.write("entries = ")
print_list(entries, "")
sys.stdout.write("\n")
