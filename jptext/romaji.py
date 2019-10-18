import re
import unicodedata
from . import charset

KEXT_NONE = 0
KEXT_MINISTRY = 1
KEXT_ANSI = 2
KEXT_HYOJUN = 4
KEXT_ALL = KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN

DIR_TO_ROMAJI = 1
DIR_FROM_ROMAJI = 2
DIR_BOTH = DIR_TO_ROMAJI | DIR_FROM_ROMAJI

ACTION_PASS = 0
ACTION_OMIT = 1
ACTION_ERROR = 2


class RomajiException(Exception):
    pass


class EncodingChangeError(RomajiException):
    pass


class Encoding(object):
    base_mapping_info = ()
    auto_sokuon = True
    romaji_regex = re.compile('(.*?)([bcdfghj-np-tv-z]*[aeiou]|n|$)([\u0300-\u036f]?)')
    hiragana_regex = re.compile('(.*?)(' + charset.hiragana.sokuonmora_re + '|$)(ー?)')
    katakana_regex = re.compile('(.*?)(' + charset.katakana.sokuonmora_re + '|$)(ー?)')
    kana_regex = re.compile(
        '(.*?)(' + charset.hiragana.sokuonmora_re + '|' + charset.katakana.sokuonmora_re + '|$)(ー?)'
    )

    def __init__(self, flags=KEXT_ALL):
        self.flags = flags
        self.k_to_r_map = {}
        self.r_to_h_map = {}
        self.r_to_k_map = {}

        for h, k, r, f in reversed(self.base_mapping_info):
            if f == KEXT_NONE or (f & flags):
                self.set_encoding(h, k, r)

    def __call__(self, flags=None):
        # This allows us to use a class or an instance of that class in the same way
        if flags is not None and flags != self.flags:
            raise EncodingChangeError("Attempt to change an encoding instance's flags after creation")
        return self

    def set_encoding(self, hiragana, katakana, romaji, direction=DIR_BOTH, auto_sokuon=None):
        if auto_sokuon is None:
            auto_sokuon = self.auto_sokuon
        self._set_encoding(hiragana, katakana, romaji, direction)
        if auto_sokuon:
            romaji = romaji[0] + romaji  # Duplicate first letter
            if hiragana:
                if hiragana[0] not in charset.hiragana.vowels:
                    hiragana = charset.hiragana.sokuon + hiragana
                else:
                    hiragana = ''
            if katakana:
                if katakana[0] not in charset.katakana.vowels:
                    katakana = charset.katakana.sokuon + katakana
                else:
                    katakana = ''
            if hiragana or katakana:
                self._set_encoding(hiragana, katakana, romaji, direction)

    def _set_encoding(self, hiragana, katakana, romaji, direction):
        if hiragana:
            if direction & DIR_TO_ROMAJI:
                self.k_to_r_map[hiragana] = romaji
            if direction & DIR_FROM_ROMAJI:
                self.r_to_h_map[romaji] = hiragana
        if katakana:
            if direction & DIR_TO_ROMAJI:
                self.k_to_r_map[katakana] = romaji
            if direction & DIR_FROM_ROMAJI:
                self.r_to_k_map[romaji] = katakana

    def hiragana_to_romaji(self, text, on_invalid=ACTION_PASS, macron=None):
        return Encoder(self.hiragana_regex, self.k_to_r_map, macron=macron).encode(text)

    def katakana_to_romaji(self, text, on_invalid=ACTION_PASS, macron=None):
        return Encoder(self.katakana_regex, self.k_to_r_map, macron=macron).encode(text)

    def kana_to_romaji(self, text, on_invalid=ACTION_PASS, macron=None):
        return Encoder(self.kana_regex, self.k_to_r_map, macron=macron).encode(text)

    def romaji_to_hiragana(self, text, on_invalid=ACTION_PASS, macron='\u0302\u0303\u0304\u0305'):
        return Decoder(self.romaji_regex, self.r_to_h_map, macrons=macron).decode(text)

    def romaji_to_katakana(self, text, on_invalid=ACTION_PASS, macron='\u0302\u0303\u0304\u0305'):
        return Decoder(self.romaji_regex, self.r_to_k_map, macrons=macron).decode(text)


class Encoder(object):
    extended_vowel_map = {'a': 'a', 'i': 'i', 'u': 'u', 'e': 'e', 'o': 'ou'}  # FIXME: should come from encoding
    macron_to_vowel_map = {'o': 'u'}  # FIXME: should come from encoding

    def __init__(self, regex, mapping, macron=None):
        self.mapping = mapping
        self.regex = regex
        self.macron = macron
        self.prev_char = None

    def encode(self, text):
        text = self.regex.sub(self._transform_match, text)
        text = unicodedata.normalize('NFC', text)
        return text

    def _transform_match(self, match):
        pre, text, post = match.groups()
        text = self.mapping.get(text, text)
        if self.macron:
            if not pre and text[0] in self.extended_vowel_map.get(self.prev_char, ''):
                text = self.macron
            self.prev_char = text[-1] if not post else None
        if post:
            if self.macron:
                text += self.macron
            else:
                text += self.macron_to_vowel_map.get(text[-1], text[-1])
        return pre + text


class Decoder(object):
    extvowel_to_kana_map = {'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'う'}  # FIXME: should come from encoding

    def __init__(self, regex, mapping, macrons=''):
        self.mapping = mapping
        self.regex = regex
        self.macrons = macrons

    def decode(self, text):
        text = unicodedata.normalize('NFD', text)
        text = self.regex.sub(self._transform_match, text)
        text = unicodedata.normalize('NFC', text)
        return text

    def _transform_match(self, match):
        pre, text, post = match.groups()
        if post and post in self.macrons:
            post = self.extvowel_to_kana_map.get(text[-1], post)  # Extended vowel
        text = self.mapping.get(text, text)
        return pre + text + post


class ModifiedHepburnEncoding(Encoding):
    base_mapping_info = (
        ('あ', 'ア', 'a', KEXT_NONE),
        ('い', 'イ', 'i', KEXT_NONE),
        ('う', 'ウ', 'u', KEXT_NONE),
        ('え', 'エ', 'e', KEXT_NONE),
        ('お', 'オ', 'o', KEXT_NONE),
        ('か', 'カ', 'ka', KEXT_NONE),
        ('き', 'キ', 'ki', KEXT_NONE),
        ('く', 'ク', 'ku', KEXT_NONE),
        ('け', 'ケ', 'ke', KEXT_NONE),
        ('こ', 'コ', 'ko', KEXT_NONE),
        ('きゃ', 'キャ', 'kya', KEXT_NONE),
        ('きゅ', 'キュ', 'kyu', KEXT_NONE),
        ('きょ', 'キョ', 'kyo', KEXT_NONE),
        ('さ', 'サ', 'sa', KEXT_NONE),
        ('し', 'シ', 'shi', KEXT_NONE),
        ('す', 'ス', 'su', KEXT_NONE),
        ('せ', 'セ', 'se', KEXT_NONE),
        ('そ', 'ソ', 'so', KEXT_NONE),
        ('しゃ', 'シャ', 'sha', KEXT_NONE),
        ('しゅ', 'シュ', 'shu', KEXT_NONE),
        ('しょ', 'ショ', 'sho', KEXT_NONE),
        ('た', 'タ', 'ta', KEXT_NONE),
        ('ち', 'チ', 'chi', KEXT_NONE),
        ('つ', 'ツ', 'tsu', KEXT_NONE),
        ('て', 'テ', 'te', KEXT_NONE),
        ('と', 'ト', 'to', KEXT_NONE),
        ('ちゃ', 'チャ', 'cha', KEXT_NONE),
        ('ちゅ', 'チュ', 'chu', KEXT_NONE),
        ('ちょ', 'チョ', 'cho', KEXT_NONE),
        ('な', 'ナ', 'na', KEXT_NONE),
        ('に', 'ニ', 'ni', KEXT_NONE),
        ('ぬ', 'ヌ', 'nu', KEXT_NONE),
        ('ね', 'ネ', 'ne', KEXT_NONE),
        ('の', 'ノ', 'no', KEXT_NONE),
        ('にゃ', 'ニャ', 'nya', KEXT_NONE),
        ('にゅ', 'ニュ', 'nyu', KEXT_NONE),
        ('にょ', 'ニョ', 'nyo', KEXT_NONE),
        ('は', 'ハ', 'ha', KEXT_NONE),
        ('ひ', 'ヒ', 'hi', KEXT_NONE),
        ('ふ', 'フ', 'fu', KEXT_NONE),
        ('へ', 'ヘ', 'he', KEXT_NONE),
        ('ほ', 'ホ', 'ho', KEXT_NONE),
        ('ひゃ', 'ヒャ', 'hya', KEXT_NONE),
        ('ひゅ', 'ヒュ', 'hyu', KEXT_NONE),
        ('ひょ', 'ヒョ', 'hyo', KEXT_NONE),
        ('ま', 'マ', 'ma', KEXT_NONE),
        ('み', 'ミ', 'mi', KEXT_NONE),
        ('む', 'ム', 'mu', KEXT_NONE),
        ('め', 'メ', 'me', KEXT_NONE),
        ('も', 'モ', 'mo', KEXT_NONE),
        ('みゃ', 'ミャ', 'mya', KEXT_NONE),
        ('みゅ', 'ミュ', 'myu', KEXT_NONE),
        ('みょ', 'ミョ', 'myo', KEXT_NONE),
        ('や', 'ヤ', 'ya', KEXT_NONE),
        ('ゆ', 'ユ', 'yu', KEXT_NONE),
        ('よ', 'ヨ', 'yo', KEXT_NONE),
        ('ら', 'ラ', 'ra', KEXT_NONE),
        ('り', 'リ', 'ri', KEXT_NONE),
        ('る', 'ル', 'ru', KEXT_NONE),
        ('れ', 'レ', 're', KEXT_NONE),
        ('ろ', 'ロ', 'ro', KEXT_NONE),
        ('りゃ', 'リャ', 'rya', KEXT_NONE),
        ('りゅ', 'リュ', 'ryu', KEXT_NONE),
        ('りょ', 'リョ', 'ryo', KEXT_NONE),
        ('わ', 'ワ', 'wa', KEXT_NONE),
        ('ゐ', 'ヰ', 'i', KEXT_NONE),  # FIXME
        ('ゑ', 'ヱ', 'e', KEXT_NONE),  # FIXME
        ('を', 'ヲ', 'o', KEXT_NONE),  # FIXME
        ('ん', 'ン', 'n', KEXT_NONE),
        ('が', 'ガ', 'ga', KEXT_NONE),
        ('ぎ', 'ギ', 'gi', KEXT_NONE),
        ('ぐ', 'グ', 'gu', KEXT_NONE),
        ('げ', 'ゲ', 'ge', KEXT_NONE),
        ('ご', 'ゴ', 'go', KEXT_NONE),
        ('ぎゃ', 'ギャ', 'gya', KEXT_NONE),
        ('ぎゅ', 'ギュ', 'gyu', KEXT_NONE),
        ('ぎょ', 'ギョ', 'gyo', KEXT_NONE),
        ('ざ', 'ザ', 'za', KEXT_NONE),
        ('じ', 'ジ', 'ji', KEXT_NONE),
        ('ず', 'ズ', 'zu', KEXT_NONE),
        ('ぜ', 'ゼ', 'ze', KEXT_NONE),
        ('ぞ', 'ゾ', 'zo', KEXT_NONE),
        ('じゃ', 'ジャ', 'ja', KEXT_NONE),
        ('じゅ', 'ジュ', 'ju', KEXT_NONE),
        ('じょ', 'ジョ', 'jo', KEXT_NONE),
        ('だ', 'ダ', 'da', KEXT_NONE),
        ('ぢ', 'ヂ', 'ji', KEXT_NONE),
        ('づ', 'ヅ', 'zu', KEXT_NONE),
        ('で', 'デ', 'de', KEXT_NONE),
        ('ど', 'ド', 'do', KEXT_NONE),
        ('ぢゃ', 'ヂャ', 'ja', KEXT_NONE),
        ('ぢゅ', 'ヂュ', 'ju', KEXT_NONE),
        ('ぢょ', 'ヂョ', 'jo', KEXT_NONE),
        ('ば', 'バ', 'ba', KEXT_NONE),
        ('び', 'ビ', 'bi', KEXT_NONE),
        ('ぶ', 'ブ', 'bu', KEXT_NONE),
        ('べ', 'ベ', 'be', KEXT_NONE),
        ('ぼ', 'ボ', 'bo', KEXT_NONE),
        ('びゃ', 'ビャ', 'bya', KEXT_NONE),
        ('びゅ', 'ビュ', 'byu', KEXT_NONE),
        ('びょ', 'ビョ', 'byo', KEXT_NONE),
        ('ぱ', 'パ', 'pa', KEXT_NONE),
        ('ぴ', 'ピ', 'pi', KEXT_NONE),
        ('ぷ', 'プ', 'pu', KEXT_NONE),
        ('ぺ', 'ペ', 'pe', KEXT_NONE),
        ('ぽ', 'ポ', 'po', KEXT_NONE),
        ('ぴゃ', 'ピャ', 'pya', KEXT_NONE),
        ('ぴゅ', 'ピュ', 'pyu', KEXT_NONE),
        ('ぴょ', 'ピョ', 'pyo', KEXT_NONE),
        ('', 'イィ', 'yi', KEXT_HYOJUN),
        ('', 'イェ', 'ye', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ウァ', 'wa', KEXT_ANSI),
        ('', 'ウィ', 'wi', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ウゥ', 'wu', KEXT_HYOJUN),
        ('', 'ウェ', 'we', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ウォ', 'wo', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ウュ', 'wyu', KEXT_ANSI),
        ('', 'ヴァ', 'va', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ヴィ', 'vi', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ヴ', 'vu', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ヴェ', 've', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ヴォ', 'vo', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ヴャ', 'vya', KEXT_ANSI),
        ('', 'ヴュ', 'vyu', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ヴィェ', 'vye', KEXT_ANSI),
        ('', 'ヴョ', 'vyo', KEXT_ANSI),
        ('', 'ヴヰ', 'vi', KEXT_ANSI),
        ('', 'ヴヲ', 'vo', KEXT_ANSI),
        ('', 'キェ', 'kye', KEXT_ANSI),
        ('', 'ギェ', 'gye', KEXT_ANSI),
        ('', 'クァ', 'kwa', KEXT_ANSI),
        ('', 'クィ', 'kwi', KEXT_ANSI),
        ('', 'クェ', 'kwe', KEXT_ANSI),
        ('', 'クォ', 'kwo', KEXT_ANSI),
        ('', 'クァ', 'qua', KEXT_MINISTRY),
        ('', 'クィ', 'qui', KEXT_MINISTRY),
        ('', 'クェ', 'que', KEXT_MINISTRY),
        ('', 'クォ', 'quo', KEXT_MINISTRY),
        ('', 'クヮ', 'kwa', KEXT_ANSI),
        ('', 'グァ', 'gwa', KEXT_ANSI),
        ('', 'グァ', 'gua', KEXT_MINISTRY),
        ('', 'グィ', 'gwi', KEXT_ANSI),
        ('', 'グェ', 'gwe', KEXT_ANSI),
        ('', 'グォ', 'gwo', KEXT_ANSI),
        ('', 'グヮ', 'gwa', KEXT_ANSI),
        ('', 'ゲォ', 'geo', KEXT_ANSI),
        ('', 'ゲョ', 'geyo', KEXT_ANSI),
        ('', 'シェ', 'she', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ジェ', 'je', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'スィ', 'si', KEXT_HYOJUN),
        ('', 'ズィ', 'zi', KEXT_HYOJUN),
        ('', 'チェ', 'che', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ツァ', 'tsa', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ツィ', 'tsi', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ツェ', 'tse', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ツォ', 'tso', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ツュ', 'tsyu', KEXT_ANSI),
        ('', 'ティ', 'ti', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'トゥ', 'tu', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'テュ', 'tyu', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ディ', 'di', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'ドゥ', 'du', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'デュ', 'dyu', KEXT_ANSI),
        ('', 'デュ', 'du', KEXT_MINISTRY),
        ('', 'ニェ', 'nye', KEXT_ANSI),
        ('', 'ヒェ', 'hye', KEXT_ANSI),
        ('', 'ビェ', 'bye', KEXT_ANSI),
        ('', 'ピェ', 'pye', KEXT_ANSI),
        ('', 'ファ', 'fa', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'フィ', 'fi', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'フェ', 'fe', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'フォ', 'fo', KEXT_MINISTRY | KEXT_ANSI | KEXT_HYOJUN),
        ('', 'フャ', 'fya', KEXT_ANSI),
        ('', 'フュ', 'fyu', KEXT_MINISTRY | KEXT_ANSI),
        ('', 'フィェ', 'fye', KEXT_ANSI),
        ('', 'フョ', 'fyo', KEXT_ANSI),
        ('', 'ホゥ', 'hu', KEXT_HYOJUN),
        ('', 'ミェ', 'mye', KEXT_ANSI),
        ('', 'リェ', 'rye', KEXT_ANSI),
        ('', 'ラ゜', 'la', KEXT_HYOJUN),
        ('', 'リ゜', 'li', KEXT_HYOJUN),
        ('', 'ル゜', 'lu', KEXT_HYOJUN),
        ('', 'レ゜', 'le', KEXT_HYOJUN),
        ('', 'ロ゜', 'lo', KEXT_HYOJUN),
        ('', 'リ゜ャ', 'lya', KEXT_HYOJUN),
        ('', 'リ゜ュ', 'lyu', KEXT_HYOJUN),
        ('', 'リ゜ェ', 'lye', KEXT_HYOJUN),
        ('', 'リ゜ョ', 'lyo', KEXT_HYOJUN),
        ('', 'ヷ', 'va', KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ヸ', 'vi', KEXT_ANSI | KEXT_HYOJUN),
        ('', 'ヹ', 've', KEXT_ANSI),
        ('', 'ヺ', 'vo', KEXT_ANSI),
    )


_default_encoding = ModifiedHepburnEncoding()


def kana_to_romaji(text, on_invalid=ACTION_PASS, macron=None):
    return _default_encoding.kana_to_romaji(text, on_invalid=on_invalid, macron=macron)
