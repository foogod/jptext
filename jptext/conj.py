from __future__ import unicode_literals

from . import jmdict as jmd

_form_aliases = {
    'np':    ('non-past', 'present', 'future', 'perfective', 'terminal', 'shuushikei', '終止形'),
    'p':     ('past', 'imperfective'),
    'te':    ('gerunditive', ),
    'mstem': ('masu-stem', 'continuative', "ren'youkei", 'renyoukei', '連用形'),
    'v':     ('volitional', ),
    'pas':   ('passive', ),
    'c':     ('causative', ),
    'pot':   ('potential', ),
    'i':     ('imperative', ),
    'ba':    ('conditional', 'conditional-ba', 'provisional-conditional'),
    'tara':  ('conditional-tara', 'past-conditional'),
}

#TODO: volitional, potential, passive, causative, imperative, conditional, conditional-tara
# Stems:
#   Irrealis form (未然形 mizenkei) -a (and -ō)
# x Continuative form (連用形 ren'yōkei) -i
# x Terminal form (終止形 shūshikei) -u
#   Attributive form (連体形 rentaikei) -u
#   Hypothetical form (仮定形 kateikei) -e
#   Imperative form (命令形 meireikei) -e


_verb_endings = {
    'snp': {
        '': 'る',
        'す': 'す',
        'く': 'く',
        'ぐ': 'ぐ',
        'む': 'む',
        'ぶ': 'ぶ',
        'ぬ': 'ぬ',
        'る': 'る',
        'う': 'う',
        'つ': 'つ',
        'ある': 'ある',
        'くる': 'くる',
        'です': 'だ',
    },
    'nsnp': {
        '': 'ない',
        'す': 'さない',
        'く': 'かない',
        'ぐ': 'がない',
        'む': 'まない',
        'ぶ': 'ばない',
        'ぬ': 'なない',
        'る': 'らない',
        'う': 'わない',
        'つ': 'たない',
        'ある': 'ない',
        'くる': 'こない',
        'です': 'ではない',
    },
    'nsnpi': {
        '': 'ない',
        'す': 'さない',
        'く': 'かない',
        'ぐ': 'がない',
        'む': 'まない',
        'ぶ': 'ばない',
        'ぬ': 'なない',
        'る': 'らない',
        'う': 'わない',
        'つ': 'たない',
        'ある': 'ない',
        'くる': 'こない',
        'です': 'じゃない',
    },
    'sp': {
        '': 'た',
        'す': 'した',
        'く': 'いた',
        'ぐ': 'いた',
        'む': 'んだ',
        'ぶ': 'んだ',
        'ぬ': 'んだ',
        'る': 'った',
        'う': 'った',
        'つ': 'った',
        'ある': 'あった',
        'いく': 'った',
        'くる': 'きた',
        'です': 'だった',
    },
    'nsp': {
        '': 'なかった',
        'す': 'さなかった',
        'く': 'かなかった',
        'ぐ': 'がなかった',
        'む': 'まなかった',
        'ぶ': 'ばなかった',
        'ぬ': 'ななかった',
        'る': 'らなかった',
        'う': 'わなかった',
        'つ': 'たなかった',
        'ある': 'なかった',
        'くる': 'こなかった',
        'です': 'じゃなかった',
    },
    'nspi': {
        '': 'なかった',
        'す': 'さなかった',
        'く': 'かなかった',
        'ぐ': 'がなかった',
        'む': 'まなかった',
        'ぶ': 'ばなかった',
        'ぬ': 'ななかった',
        'る': 'らなかった',
        'う': 'わなかった',
        'つ': 'たなかった',
        'ある': 'なかった',
        'くる': 'こなかった',
        'です': 'ではなかった',
    },
    'pnp': {
        '': 'ます',
        'す': 'します',
        'く': 'きます',
        'ぐ': 'ぎます',
        'む': 'みます',
        'ぶ': 'びます',
        'ぬ': 'にます',
        'る': 'ります',
        'う': 'います',
        'つ': 'ちます',
        'ある': 'あります',
        'くる': 'きます',
        'です': 'です',
    },
    'npnp': {
        '': 'ません',
        'す': 'しません',
        'く': 'きません',
        'ぐ': 'ぎません',
        'む': 'みません',
        'ぶ': 'びません',
        'ぬ': 'にません',
        'る': 'りません',
        'う': 'いません',
        'つ': 'ちません',
        'ある': 'ありません',
        'くる': 'きません',
        'です': 'ではありません',
    },
    'npnpi': {
        '': 'ないです',
        'す': 'しないです',
        'く': 'きないです',
        'ぐ': 'ぎないです',
        'む': 'みないです',
        'ぶ': 'びないです',
        'ぬ': 'にないです',
        'る': 'りないです',
        'う': 'いないです',
        'つ': 'ちないです',
        'ある': 'ないです',
        'くる': 'こないです',
        'です': 'じゃないです',
    },
    'pp': {
        '': 'ました',
        'す': 'しました',
        'く': 'きました',
        'ぐ': 'ぎました',
        'む': 'みました',
        'ぶ': 'びました',
        'ぬ': 'にました',
        'る': 'りました',
        'う': 'いました',
        'つ': 'ちました',
        'ある': 'ありました',
        'くる': 'きました',
        'です': 'でした',
    },
    'npp': {
        '': 'ませんでした',
        'す': 'しませんでした',
        'く': 'きませんでした',
        'ぐ': 'ぎませんでした',
        'む': 'みませんでした',
        'ぶ': 'びませんでした',
        'ぬ': 'にませんでした',
        'る': 'りませんでした',
        'う': 'いませんでした',
        'つ': 'ちませんでした',
        'ある': 'ありませんでした',
        'くる': 'きませんでした',
        'です': 'ではありませんでした',
    },
    'nppi': {
        '': 'なかったです',
        'す': 'さなかったです',
        'く': 'かなかったです',
        'ぐ': 'がなかったです',
        'む': 'まなかったです',
        'ぶ': 'ばなかったです',
        'ぬ': 'ななかったです',
        'る': 'らなかったです',
        'う': 'わなかったです',
        'つ': 'たなかったです',
        'ある': 'なかったです',
        'くる': 'こなかったです',
        'です': 'じゃなかったです',
    },
    'te': {
        '': 'て',
        'す': 'して',
        'く': 'いて',
        'ぐ': 'いて',
        'む': 'んで',
        'ぶ': 'んで',
        'ぬ': 'んで',
        'る': 'って',
        'う': 'って',
        'つ': 'って',
        'いく': 'って',
        'ある': 'あって',
        'くる': 'きて',
        'です': 'で',
    },
    'nte': {
        '': 'なくて',
        'す': 'さなくて',
        'く': 'かなくて',
        'ぐ': 'がなくて',
        'む': 'まなくて',
        'ぶ': 'ばなくて',
        'ぬ': 'ななくて',
        'る': 'らなくて',
        'う': 'わなくて',
        'つ': 'たなくて',
        'ある': 'なくて',
        'くる': 'こなくて',
        'です': 'ではなくて',
    },
    'ntei': {
        '': 'なくて',
        'す': 'さなくて',
        'く': 'かなくて',
        'ぐ': 'がなくて',
        'む': 'まなくて',
        'ぶ': 'ばなくて',
        'ぬ': 'ななくて',
        'る': 'らなくて',
        'う': 'わなくて',
        'つ': 'たなくて',
        'ある': 'なくて',
        'くる': 'こなくて',
        'です': 'じゃなくて',
    },
    'mstem': {
        '': '',
        'す': 'し',
        'く': 'き',
        'ぐ': 'ぎ',
        'む': 'み',
        'ぶ': 'び',
        'ぬ': 'に',
        'る': 'り',
        'う': 'い',
        'つ': 'ち',
        'ある': 'あり',
        'くる': 'き',
        'です': 'で',  # Note: not technically correct (だ/です does not have a ren'youkei form), but the closest equivalent (for continuative, etc)
    },
    '': {
        '': '',
        'す': '',
        'く': '',
        'ぐ': '',
        'む': '',
        'ぶ': '',
        'ぬ': '',
        'る': '',
        'う': '',
        'つ': '',
        'ある': '',
        'くる': '',
        'です': '',
    },
}

_form_lookup = {a: f for f, k in _form_aliases.items() for a in k}

class UnsupportedException (Exception):
    pass


def verb_form_id(form, negative=False, polite=False, informal=False):
    form = _form_lookup.get(form, form)
    if form not in ('mstem', 'np', 'p', 'te'):
        raise ValueError("Unknown verb form/tense: {!r}".format(form))

    if form == 'mstem':
        return form

    name = []
    if negative:
        name.append('n')
    if form in ('np', 'p'):
        if polite:
            name.append('p')
        else:
            name.append('s')
    name.append(form)
    if negative and informal:
        name.append('i')

    return ''.join(name)

def _conj_verb_ichidan(word, form):
    return word[:-1] + _verb_endings[form]['']

def _conj_verb_godan(word, form):
    try:
        return word[:-1] + _verb_endings[form][word[-1]]
    except KeyError:
        raise ValueError("Bad verb ending for godan verb: {!r}".format(word))

def _conj_verb_aru(word, form):
    if word.endswith('ある'):
        # kana form. We can just use the table directly.
        return word[:-2] + _verb_endings[form]['ある']
    else:
        # kanji form. We actually need to change the kanji for some variants.
        prefix = word[:-2]
        kanji = word[-2]
        kana_form = _verb_endings[form]['ある']
        ending_type = kana_form[0]
        ending = kana_form[1:]
        if ending_type == 'な':
            kanji = '無'
        return prefix + kanji + ending

def _conj_verb_iku(word, form):
    # This word behaves like a normal く-verb, with a couple of exceptions
    return word[:-1] + _verb_endings[form].get('いく', _verb_endings[form]['く'])

def _conj_verb_suru(word, form):
    # する actually conjugates the same as an ichidan verb, with the exception
    # that in kana form the stem changes to し instead of す for everything
    # except the snp form.
    if word.endswith('する') and form != 'snp':
        stem = word[:-2] + 'し'
    else:
        stem = word[:-1]
    return stem + _verb_endings[form]['']

def _conj_verb_kuru(word, form):
    # くる is technically irregular, but it only shows up in its kana form
    # (kanji forms appear like normal ichidan conjugation)
    if word.endswith('くる'):
        return word[:-2] + _verb_endings[form]['くる']
    return word[:-1] + _verb_endings[form]['']

def _conj_verb_desu(word, form):
    # The "dictionary form" is usually です, but the simple-non-past (which is
    # the same as the dictionary form for all other words) is だ, so accept
    # either form here.
    if word.endswith('です'):
        return word[:-2] + _verb_endings[form]['です']
    if word.endswith('だ'):
        return word[:-1] + _verb_endings[form]['です']
    raise ValueError("Do not know how to conjugate {!r} as a copula".format(word))

def conj_verb(word, form, verb_type=None, jmdict=None):
    if isinstance(form, dict):
        form = verb_form_id(**form)
    if not verb_type:
        # We want to accept 'です' as a form of the copula, but JMDict only has
        # 'だ' ('です' is present, but is considered an "expression", not a
        # copula/verb), so we special-case this and hardcode it as a workaround
        if word == 'です':
            verb_type = 'copula'
        else:
            if not jmdict:
                jmdict = jmd._default_jmdict()
            try:
                entries = jmdict.lookup(word)
            except KeyError:
                raise ValueError("The word {!r} is unknown.  Cannot determine verb type.".format(word)) from None
            for e in entries:
                for p in e.pos_details:
                    if p['cat'] == 'verb':
                        verb_type = p['subcat']
                        break
                if verb_type:
                    break
            if not verb_type:
                raise ValueError("The word {!r} is not a verb or its type cannot be determined.".format(word))

    if verb_type == 'ichidan':
        return _conj_verb_ichidan(word, form)
    if verb_type == 'godan':
        return _conj_verb_godan(word, form)
    if verb_type in ('irregular', 'copula', 'suru', 'kuru'):
        if word in ('です', 'だ'):
            return _conj_verb_desu(word, form)
        ending = word[-2:]
        if ending in ('ある', '有る', '在る'):
            return _conj_verb_aru(word, form)
        if ending in ('いく', 'ゆく', '行く', '逝く', '往く', 'てく', 'でく'):
            return _conj_verb_iku(word, form)
        if ending in ('する', '為る'):
            return _conj_verb_suru(word, form)
        if ending in ('くる', '来る'):
            return _conj_verb_kuru(word, form)
        ending = word[-1:]
        if ending in ('り'):
            raise UnsupportedException("Conjugating irregular り-verbs is not currently supported: {!r}".format(word))
        raise UnsupportedException("Unrecognized irregular verb type: {!r}".format(word))
    if verb_type in ('nidan', 'yodan'):
        raise UnsupportedException("Conjugating {} verbs is not currently supported.".format(verb_type))
    raise ValueError("Uknwnown verb type: {!r}".format(verb_type))

