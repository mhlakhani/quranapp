class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '\xd0\xcc\xeeS\x0c\x0b\xffCH\xff\x9f\x9cG"m\xdde.\r\x02\x043-\xb4'
    DB_SURAH_KEY = 'quranapp:surahs'
    DB_AYAT_KEY = 'quranapp:ayats'

class DevelopmentConfig(DefaultConfig):
    DEBUG = True

class TestingConfig(DefaultConfig):
    TESTING = True
