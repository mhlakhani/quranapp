from quranapp import app
from flask import g, abort
from math import ceil
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Pagination(object):

    def __init__(self, items, page, per_page, total_count):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

class Surah(object):

    def __init__(self, id, name_arabic, name_english, name_english_transliterated, start_ayat, num_ayats):
        self.id = id
        self.name_arabic = name_arabic
        self.name_english = name_english
        self.name_english_transliterated = name_english_transliterated
        self.start_ayat = start_ayat
        self.num_ayats = num_ayats

    def save(self):
        st = pickle.dumps(self)
        g.redis.hset(app.config['DB_SURAH_KEY'], self.id, st)

    def get_ayats(self, page, per_page):
        start = (page - 1) * per_page
        if start > self.num_ayats:
            abort(404)
        end = min(start + per_page, self.num_ayats)
        start += self.start_ayat
        end += self.start_ayat
        items = g.redis.hmget(app.config['DB_AYAT_KEY'], [x for x in xrange(start, end)])
        items = map(pickle.loads, items)
        return Pagination(items, page, per_page, self.num_ayats)

    def __repr__(self):
        return '<Surah %s: %s>' % (self.id, self.name_english)

    @staticmethod
    def get(id):
        st = g.redis.hget(app.config['DB_SURAH_KEY'], id)
        return pickle.loads(st)
    
    @staticmethod
    def get_or_404(id):
        st = g.redis.hget(app.config['DB_SURAH_KEY'], id)
        if st is None:
            abort(404)
        return pickle.loads(st)

    @staticmethod
    def get_all():
        ret = g.redis.hgetall(app.config['DB_SURAH_KEY'])
        lis = ret.items()
        lis.sort(key = lambda x: int(x[0]))
        return map(pickle.loads, [x[1] for x in lis])

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
        g.redis.hset(app.config['DB_AYAT_KEY'], self.id, st)

    def __repr__(self):
        return '<Surah %s Ayat %s>' % (self.surah_id, self.number)

    @staticmethod
    def get(id):
        st = g.redis.hget(app.config['DB_AYAT_KEY'], id)
        return pickle.loads(st)

    @staticmethod
    def get_many(ids):
        return map(pickle.loads, [x for x in g.redis.hmget(app.config['DB_AYAT_KEY'], ids) if x is not None])
