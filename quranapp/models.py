from quranapp import app
from flask import g
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Surah(object):

    def __init__(self, id, name_arabic, name_english, name_english_transliterated, num_ayats):

        self.id = id
        self.name_arabic = name_arabic
        self.name_english = name_english
        self.name_english_transliterated = name_english_transliterated
        self.num_ayats = num_ayats

    def save(self):

        st = pickle.dumps(self)
        g.redis.hset('quranapp:surahs', self.id, st)

    def __repr__(self):
        return '<Surah %s: %s>' % (self.id, self.name_english)

    @staticmethod
    def get(id):

        st = g.redis.hget('quranapp:surahs', id)
        return pickle.loads(st)

class Ayat(object):

    def __init__(self, id, surah_id, number, arabic, english, bismillah):

        self.id = id
        self.surah_id = surah_id
        self.number = number
        self.arabic = arabic
        self.english = english
        self.bismillah = bismillah

    def save(self):

        st = pickle.dumps(self)
        g.redis.hset('quranapp:ayats', self.id, st)

    def __repr__(self):
        return '<Surah %s Ayat %s>' % (self.surah_id, self.number)

    @staticmethod
    def get(id):

        st = g.redis.hget('quranapp:ayats', id)
        return pickle.loads(st)
