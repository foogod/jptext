# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unicodedata
import re


class CharacterSet(object):
    pass


class halfwidth(CharacterSet):
    ascii = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    space = " "
    numbers = "0123456789"
    punctuation = "｡｢｣､ !\"#$%&'()*+,-./:;<=>?@`{|}~"
    re_range_numbers = "\u0030-\u0039"
    re_range_punct = "\uff61-\uff64" + "\u0020-\u002f" + "\u003a-\u0040" + "\u0060" + "\u007b-\u007e"


class fullwidth(CharacterSet):
    ascii = "\u3000！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～"
    space = "\u3000"
    numbers = "０１２３４５６７８９"
    punctuation = "、。〃〄〆〇〈〉《》「」『』【】〒〓〔〕〖〗〘〙〚〛〜〝〞〟〠〡〢〣〤〥〦〧〨〩〪〭〮〯〫〬〰〱〲〳〴〵〶〷〸〹〺〻〼〽〾！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠｀｛｜｝～｟｠"
    re_range_numbers = "\uff10-\uff19"
    # Note: U+3004 ('々') is in the punctuation range, but is really
    # effectively a word-character, so shouldn't be counted as punctuation.
    re_range_punct = "\u3001-\u3004" + "\u3006-\u303e" + "\uff01-\uff0f" + "\uff1a-\uff20" + "\uff40" + "\uff5b-\uff60"


all_numbers = fullwidth.numbers + halfwidth.numbers
all_punctuation = fullwidth.punctuation + halfwidth.punctuation
re_range_all_numbers = fullwidth.re_range_numbers + halfwidth.re_range_numbers
re_range_all_punct = fullwidth.re_range_punct + halfwidth.re_range_punct


class KanaCharacterSet(CharacterSet):
    pass


class hiragana(KanaCharacterSet):
    _trans_set = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ゛゜・ーゝゞ"
    all = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ゛゜ゝゞゟ"
    large = "あいうえおかがきぎくぐけげこごさざしじすずせぜそぞただちぢつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもやゆよらりるれろわゐゑをんゔ"
    small = "ぁぃぅぇぉっゃゅょゎゕゖ"
    ligatures = "ゟ"
    combining = "ぁぃぅぇぉゃゅょゎ"
    small_non_combining = "ゕゖ"
    vowels = "あいうえお"
    sokuon = "っ"
    hybrid_sokuon = "ッ"  # (See note below)
    stresses = "゛゜"
    intraword = "・ー"
    repeats = "ゝゞ"
    period = "。"
    comma = "、"
    quotes = "「」"
    re_range_block = "\u3040-\u309f"
    re_range_nosym = "\u3040-\u3096" + "\u309f"
    re_range = re_range_block + fullwidth.re_range_punct
    mora_re = (
        ("[" + large + small_non_combining + ligatures + repeats + sokuon + intraword + "]")
        + ("[" + stresses + "]?")
        + ("[" + combining + "]?")
    )
    sokuonmora_re = (
        (sokuon + "?[" + large + "][" + stresses + "]?[" + combining + "]?")
        + "|"
        + ("[" + small_non_combining + ligatures + repeats + intraword + "]")
    )
    # Occasionally, some words will be spelled in katakana with a final bit
    # (usually と) in hiragana.  In these cases, if there is a sokuon before
    # the final bit, the sokuon is often katakana, but the next mora is
    # hiragana, which the normal sokuonmora_re will not handle.  The following
    # correctly matches those cases as well:
    hybrid_sokuonmora_re = (
        ("[" + sokuon + hybrid_sokuon + "]?[" + large + "][" + stresses + "]?[" + combining + "]?")
        + "|"
        + ("[" + small_non_combining + ligatures + repeats + intraword + "]")
    )


class katakana(KanaCharacterSet):
    _trans_set = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ゛゜・ーヽヾ"
    all = "゛゜゠ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヷヸヹヺ・ーヽヾヿ"
    large = "アイウエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワヰヱヲンヴヷヸヹヺ"
    small = "ァィゥェォッャュョヮヵヶ"
    ligatures = "ヿ"
    combining = "ァィゥェォャュョヮ"
    small_non_combining = "ヵヶ"
    vowels = "アイウエオ"
    sokuon = "ッ"
    hybrid_sokuon = "っ"  # (See note below)
    stresses = "゛゜"
    intraword = "゠・ー"
    repeats = "ヽヾ"
    period = "。"
    comma = "、"
    quotes = "「」"
    re_range_block = "\u30a0-\u30ff"
    # Note: We include 'ー' in the "nosym" range because even though it is
    # technically a symbol, it is really a "word character" (not a separator)
    # in the context of katakana words.
    re_range_nosym = "\u30a1-\u30fa" + "\u30fc" + "\u30ff"
    re_range = "\u309b" + "\u309c" + re_range_block + fullwidth.re_range_punct
    mora_re = (
        ("[" + large + small_non_combining + ligatures + repeats + sokuon + intraword + "]")
        + ("[" + stresses + "]?")
        + ("[" + combining + "]?")
    )
    sokuonmora_re = (
        (sokuon + "?[" + large + "][" + stresses + "]?[" + combining + "]?")
        + "|"
        + ("[" + small_non_combining + ligatures + repeats + intraword + "]")
    )
    # This is to catch cases where a hiragana sokuon is followed by a katakana
    # mora.  In practice, this is not nearly as likely to happen as the other
    # way around (see hiragana.hybrid_sokuonmora_re), but this is included for completeness.
    hybrid_sokuonmora_re = (
        ("[" + sokuon + hybrid_sokuon + "]?[" + large + "][" + stresses + "]?[" + combining + "]?")
        + "|"
        + ("[" + small_non_combining + ligatures + repeats + intraword + "]")
    )


class katakana_halfwidth(KanaCharacterSet):
    _trans_set = "ｧｱｨｲｩｳｪｴｫｵｶ ｷ ｸ ｹ ｺ ｻ ｼ ｽ ｾ ｿ ﾀ ﾁ ｯﾂ ﾃ ﾄ ﾅﾆﾇﾈﾉﾊ  ﾋ  ﾌ  ﾍ  ﾎ  ﾏﾐﾑﾒﾓｬﾔｭﾕｮﾖﾗﾘﾙﾚﾛ ﾜ  ｦﾝ   ﾞﾟ･ｰ  "
    all = "･ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝﾞﾟ"
    large = "ｦｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"
    small = "ｧｨｩｪｫｬｭｮｯ"
    ligatures = ""
    combining = "ｧｨｩｪｫｬｭｮ"
    small_non_combining = ""
    vowels = "ｱｲｳｴｵ"
    sokuon = "ｯ"
    stresses = "ﾞﾟ"
    repeats = ""
    intraword = "･ｰ"
    period = "｡"
    comma = "､"
    quotes = "｢｣"
    re_range_block = "\uff65-\uff9f"
    # Note: We include 'ｰ' in the "nosym" range because even though it is
    # technically a symbol, it is really a "word character" (not a separator)
    # in the context of katakana words.
    re_range_nosym = "\uff66-\uff6f\uff70-\uff9d"
    re_range = re_range_block + halfwidth.re_range_punct
    mora_re = (
        ("[" + large + small_non_combining + ligatures + repeats + sokuon + intraword + "]")
        + ("[" + stresses + "]?")
        + ("[" + combining + "]?")
    )
    sokuonmora_re = (
        (sokuon + "?[" + large + "][" + stresses + "]?[" + combining + "]?")
        + "|"
        + ("[" + small_non_combining + ligatures + repeats + intraword + "]")
    )


class kanji(CharacterSet):
    re_range_block = "\u3400-\u4db5" + "\u4e00-\u9fcb" + "\uf900-\ufa6a"
    re_range_nosym = "\u3005" + re_range_block
    re_range = "\u3005" + re_range_block + fullwidth.re_range_punct


class jptext_fullwidth(CharacterSet):
    re_range_nosym = hiragana.re_range_nosym + katakana.re_range_nosym + kanji.re_range_nosym
    re_range = re_range_nosym + fullwidth.re_range_punct


class jptext(CharacterSet):
    re_range_nosym = jptext_fullwidth.re_range_nosym + katakana_halfwidth.re_range_nosym
    re_range = jptext_fullwidth.re_range + katakana_halfwidth.re_range


_hiragana_to_katakana_trmap = {ord(a): ord(b) for a, b in zip(hiragana._trans_set, katakana._trans_set)}
_katakana_to_hiragana_trmap = {ord(a): ord(b) for a, b in zip(katakana._trans_set, hiragana._trans_set)}
_kkfw_to_kkhw_trmap = {ord(a): ord(b) for a, b in zip(katakana._trans_set, katakana_halfwidth._trans_set) if b != " "}
_kkhw_to_kkfw_trmap = {ord(a): ord(b) for a, b in zip(katakana_halfwidth._trans_set, katakana._trans_set) if a != " "}
_asciifw_to_asciihw_trmap = {ord(a): ord(b) for a, b in zip(fullwidth.ascii, halfwidth.ascii)}
_asciihw_to_asciifw_trmap = {ord(a): ord(b) for a, b in zip(halfwidth.ascii, fullwidth.ascii)}


def hiragana_to_katakana(text):
    return text.translate(_hiragana_to_katakana_trmap)


def katakana_to_hiragana(text):
    return text.translate(_katakana_to_hiragana_trmap)


def katakana_fullwidth_to_halfwidth(text):
    text = unicodedata.normalize("NFD", text)
    text = text.translate(_kkfw_to_kkhw_trmap)
    text = unicodedata.normalize("NFC", text)
    return text


def katakana_halfwidth_to_fullwidth(text):
    text = text.translate(_kkhw_to_kkfw_trmap)
    text = unicodedata.normalize("NFC", text)
    return text


def ascii_fullwidth_to_halfwidth(text):
    return text.translate(_asciifw_to_asciihw_trmap)


def ascii_halfwidth_to_fullwidth(text):
    return text.translate(_asciihw_to_asciifw_trmap)


def jptext_portions(text, punctuation=False):
    if punctuation:
        re_range = jptext.re_range
    else:
        re_range = jptext.re_range_nosym
    rexp = re.compile('[{}]+'.format(re_range))
    return rexp.findall(text)

def is_charset(charset, text, punctuation=True):
    if punctuation:
        re_range = charset.re_range + '\s'
    else:
        re_range = charset.re_range_nosym
    rexp = re.compile('^[{}]*$'.format(re_range))
    return bool(rexp.match(text))

def is_hiragana(text, punctuation=True):
    return is_charset(hiragana, text, punctuation)

def is_katakana(text, punctuation=True):
    return is_charset(katakana, text, punctuation)

