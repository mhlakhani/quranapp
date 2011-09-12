from quranapp import app
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Surah(db.Model):
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    name_arabic = db.Column(db.Text)
    name_english = db.Column(db.Text)
    name_english_transliterated = db.Column(db.Text)
    num_ayats = db.Column(db.Integer)
    ayats = db.relationship('Ayat', backref='surah', lazy='dynamic')

    def __init__(self, id, name_arabic, name_english, name_english_transliterated, num_ayats):
        self.id = id
        self.name_arabic = name_arabic
        self.name_english = name_english
        self.name_english_transliterated = name_english_transliterated
        self.num_ayats = num_ayats

    def __repr__(self):
        return '<Surah %s: %s>' % (self.id, self.name_english)

class Ayat(db.Model):
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
    id = db.Column(db.Integer, primary_key=True)
    surah_id = db.Column(db.Integer, db.ForeignKey('surah.id'))
    number = db.Column(db.Integer)
    arabic = db.Column(db.Text)
    english = db.Column(db.Text)
    bismillah = db.Column(db.Text)

    def __init__(self, surah_id, number, arabic, english, bismillah):
        self.surah_id = surah_id
        self.number = number
        self.arabic = arabic
        self.english = english
        self.bismillah = bismillah

    def __repr__(self):
        return '<Surah %s Ayat %s>' % (self.surah_id, self.number)
