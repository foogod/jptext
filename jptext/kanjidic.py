# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class KanjiDict(object):
    def __init__(self, data=None):
        if data is None:
            from . import _kanjidic_data

            data = _kanjidic_data.characters
        self._data = data
        self.reindex()

    def reindex(self):
        self._kanji_index = {e["literal"]: e for e in self._data}
        meaning_index = {}
        for e in self._data:
            for rmg in e["reading_meaning"]["rmgroup"]:
                for lang, meanings in rmg["meaning"].items():
                    meaning_index.setdefault(lang, {})
                    for m in meanings:
                        meaning_index[lang].setdefault(m, []).append(e)
        self._meaning_index = meaning_index

    def get_kanji(self, kanji):
        return KanjiDictEntry(self._kanji_index[kanji])

    def lookup_meaning(self, lang, meaning):
        mi = self._meaning_index.get(lang, {})
        return [KanjiDictEntry(e) for e in mi.get(meaning, [])]

    def __getitem__(self, kanji):
        return self.get_kanji(kanji)

    def __repr__(self):
        return "<{}: {} entries>".format(self.__class__.__name__, len(self._data))


class KanjiDictEntry(object):
    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return "<{}: {!r}>".format(self.__class__.__name__, self.kanji)

    def __eq__(self, other):
        if not isinstance(other, KanjiDictEntry):
            return False
        return self.kanji == other.kanji

    def __gt__(self, other):
        if not isinstance(other, KanjiDictEntry):
            raise TypeError("'>' not supported between instances of {!r} and {!r}".format(type(self), type(other)))
        try:
            return self.freq > other.freq
        except TypeError:
            return False

    def __lt__(self, other):
        if not isinstance(other, KanjiDictEntry):
            raise TypeError("'<' not supported between instances of {!r} and {!r}".format(type(self), type(other)))
        try:
            return self.freq < other.freq
        except TypeError:
            return False

    @property
    def kanji(self):
        return self._data["literal"]

    @property
    def freq(self):
        return self._data["misc"].get("freq")

    @property
    def stroke_count(self):
        return self._data["misc"].get("stroke_count")

    @property
    def grade(self):
        return self._data["misc"].get("grade")

    @property
    def all_on_readings(self):
        return [r[""] for rmg in self._data["reading_meaning"]["rmgroup"] for r in rmg["reading"].get("ja_on", [])]

    @property
    def all_kun_readings(self):
        return [r[""] for rmg in self._data["reading_meaning"]["rmgroup"] for r in rmg["reading"].get("ja_kun", [])]

    @property
    def all_readings(self):
        return self.all_on_readings + self.all_kun_readings

    @property
    def nanori(self):
        return self._data["reading_meaning"]["nanori"]

    def all_meanings(self, lang="en"):
        return sum((rmg["meaning"][lang] for rmg in self._data["reading_meaning"]["rmgroup"]), [])

    @property
    def misc(self):
        return self._data["misc"]


KanjiDic = KanjiDict


_dict = None


def _default_kanjidict():
    global _dict
    if _dict is None:
        _dict = KanjiDict()
    return _dict


def get_kanji(kanji):
    return _default_kanjidict().get_kanji(kanji)


def lookup_meaning(lang, meaning):
    return _default_kanjidict().lookup_meaning(lang, meaning)
