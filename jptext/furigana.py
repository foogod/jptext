import html
import re
from . import charset
from . import kanjidic

hiragana_re = re.compile('[^' + charset.kanji.re_range_nosym + charset.katakana.re_range_nosym + ']+')


class FuriganaError(Exception):
    pass


def get_furi_re(kanji_text):
    global hiragana_re

    pattern = []
    pos = 0
    while pos < len(kanji_text):
        m = hiragana_re.search(kanji_text, pos=pos)
        if not m:
            pattern.append('(.+)()')
            break
        if m.start() == pos:
            pattern.append('()')
        else:
            pattern.append('(.+)')
        pattern.append('(' + m.group() + ')')
        pos = m.end()
    return re.compile(''.join(pattern))


def pairwise(seq):
    "[1, 2, 3, 4, ...] -> [(1, 2), (3, 4), ...]"
    i = iter(seq)
    return zip(i, i)


def cleanup_reading(text):
    text = charset.katakana_to_hiragana(text)
    text = re.sub('[^' + charset.hiragana.re_range_nosym + ']', '', text)
    return text


def get_readings(kanji_char):
    try:
        kde = kanjidic.get_kanji(kanji_char)
    except KeyError:
        return set()
    return set((cleanup_reading(r) for r in kde.all_readings))


def match_furi(kanji, furi):
    # Construct a regular expression pattern of all possible ways to read this
    # sequence of kanji (based on individual kanji readings)
    pattern = []
    for char in kanji:
        readings = get_readings(char)
        if readings:
            pattern.append('(' + '|'.join((re.escape(r) for r in readings)) + ')')
        else:
            pattern.append('(.+)')

    # We try an exact match with the full expression first.  If that doesn't
    # work, we go one level deeper and see if we can match all-but-one of the
    # kanji, in which case, we'll use that.  This catches many common cases of
    # rendaku, etc, though can theoretically result in incorrect assignments of
    # things that really should be done as a group instead.
    for i in range(-1, len(pattern)):
        p = list(pattern)
        if i >= 0:
            p[i] = '(.+)'
        m = re.match(''.join(p) + '$', furi)
        if m:
            return [pair for pair in zip(kanji, m.groups())]

    # Couldn't figure out how to match them up to individual characters at all.
    # Give up and just return it as a group.
    return [(kanji, furi)]


def apply_furi(kanji_text, hiragana_text):
    furi_re = get_furi_re(kanji_text)
    m = furi_re.match(hiragana_text)
    if not m:
        raise FuriganaError("Unable to match {!r} to {!r}".format(kanji_text, hiragana_text))
    result = []
    k_start = 0
    for furi, hira in pairwise(m.groups()):
        if hira:
            k_end = kanji_text.index(hira, k_start)
            k_seq = kanji_text[k_start:k_end]
            if k_seq:
                result.extend(match_furi(k_seq, furi))
            result.append((hira, None))
            k_start = k_end + len(hira)
        else:
            # This will only happen at the end of the string
            k_seq = kanji_text[k_start:]
            result.extend(match_furi(k_seq, furi))
    return result


def furi_html(kanji_text, hiragana_text):
    result = ['<ruby>']
    for kanji, furi in apply_furi(kanji_text, hiragana_text):
        result.append('<rb>{}</rb><rt>{}</rt>'.format(html.escape(kanji), html.escape(furi or '')))
    result.append('</ruby>')
    return ''.join(result)
