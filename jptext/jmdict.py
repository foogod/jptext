# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class JMDict(object):
    def __init__(self, data=None):
        if data is None:
            from . import _jmdict_data

            data = _jmdict_data.entries
        self._data = data
        self.reindex()

    def reindex(self):
        kanji_index = {}
        kana_index = {}
        for entry in self._data:
            for k in entry["k_ele"]:
                kanji_index.setdefault(k["keb"], []).append(entry)
            for r in entry["r_ele"]:
                kana_index.setdefault(r["reb"], []).append(entry)
        self._kanji_index = kanji_index
        self._kana_index = kana_index

    def lookup_kanji(self, kanji):
        return [JMDictEntry(entry) for entry in self._kanji_index[kanji]]

    def lookup_kana(self, kana):
        return [JMDictEntry(entry) for entry in self._kana_index[kana]]

    def lookup(self, word):
        try:
            return self.lookup_kanji(word)
        except KeyError:
            pass
        return self.lookup_kana(word)

    def entries(self):
        return (JMDictEntry(entry) for entry in self._data)

    def __repr__(self):
        return "<{}: {} entries>".format(self.__class__.__name__, len(self._data))


class JMDictEntry(object):
    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return "<{}: {!r}>".format(self.__class__.__name__, self.ent_seq)

    def __eq__(self, other):
        if not isinstance(other, JMDictEntry):
            return False
        return self.ent_seq == other.ent_seq

    def __gt__(self, other):
        if not isinstance(other, JMDictEntry):
            raise TypeError("'>' not supported between instances of {!r} and {!r}".format(type(self), type(other)))
        try:
            return self.ent_seq > other.ent_seq  # FIXME
        except TypeError:
            return False

    def __lt__(self, other):
        if not isinstance(other, JMDictEntry):
            raise TypeError("'<' not supported between instances of {!r} and {!r}".format(type(self), type(other)))
        try:
            return self.ent_seq < other.ent_seq  # FIXME
        except TypeError:
            return False

    @property
    def ent_seq(self):
        return self._data["ent_seq"]

    @property
    def kanji(self):
        return [k["keb"] for k in self._data["k_ele"]]

    @property
    def readings(self):
        return [r["reb"] for r in self._data["r_ele"]]

    @property
    def senses(self):
        return [JMDictSense(self, sense) for sense in self._data["sense"]]

    @property
    def pos_details(self):
        results = []
        for sense in self._data["sense"]:
            for pd in sense["pos_details"]:
                if pd not in results:
                    results.append(pd)
        #FIXME: make this immutable?
        return results


class JMDictSense(object):
    def __init__(self, entry, data):
        self.entry = entry
        self._data = data

    def __repr__(self):
        return "<{}: {!r}>".format(self.__class__.__name__, self.entry.ent_seq)

    @property
    def pos(self):
        return tuple(self._data["pos"])

    @property
    def pos_details(self):
        #FIXME: make this immutable?
        return self._data["pos_details"]


_dict = None


def _default_jmdict():
    global _dict
    if _dict is None:
        _dict = JMDict()
    return _dict


def lookup_kanji(kanji):
    return _default_jmdict().lookup_kanji(kanji)
