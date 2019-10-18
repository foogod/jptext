# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unicodedata


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
    punctuation = "、。〃〄々〆〇〈〉《》「」『』【】〒〓〔〕〖〗〘〙〚〛〜〝〞〟〠〡〢〣〤〥〦〧〨〩〪〭〮〯〫〬〰〱〲〳〴〵〶〷〸〹〺〻〼〽〾！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠｀｛｜｝～｟｠"
    re_range_numbers = "\uff10-\uff19"
    re_range_punct = "\u3001-\u303e" + "\uff01-\uff0f" + "\uff1a-\uff20" + "\uff40" + "\uff5b-\uff60"


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
    stresses = "゛゜"
    intraword = "゠・ー"
    repeats = "ヽヾ"
    period = "。"
    comma = "、"
    quotes = "「」"
    re_range_block = "\u30a0-\u30ff"
    re_range_nosym = "\u30a1-\u30fa" + "\u30ff"
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
    re_range_nosym = "\uff66-\uff6f\uff71-\uff9d"
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
