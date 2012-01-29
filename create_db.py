import quranapp
from quranapp.models import *
import os
from BeautifulSoup import BeautifulStoneSoup
from flask import g
import redis

def add_surahs():
    print 'Adding Surahs'
    fil = open(os.path.join(os.getcwd(), 'data', 'quran-data.xml'))
    soup = BeautifulStoneSoup(fil)
    entries = soup.find('quran').find('suras').findAll('sura')
    start_ayat = 1
    for entry in entries:
        id = int(entry['index'])
        name_arabic = entry['name']
        name_english = entry['ename']
        name_english_transliterated = entry['tname']
        num_ayats = int(entry['ayas'])
        surah = Surah(id, name_arabic, name_english, name_english_transliterated, start_ayat, num_ayats)
        surah.save()
        start_ayat += num_ayats
    fil.close()

def create_end_of_ayat(num):
    digs = [unichr(1632 + int(d)) for d in str(num)]
    return ' ' + unichr(8238) + unichr(1757) + ''.join(digs) + unichr(8236)

def add_ayats():
    print 'Adding Ayats'
    fil_arabic = open(os.path.join(os.getcwd(), 'data', 'quran-uthmani.xml'))
    fil_english = open(os.path.join(os.getcwd(), 'data', 'en.hilali.xml'))
    soup_arabic = BeautifulStoneSoup(fil_arabic)
    soup_english = BeautifulStoneSoup(fil_english)
    id = 1
    for surah_id in xrange(1,115):
        print 'Parsing Surah %s' % surah_id
        dat_arabic = soup_arabic.find('quran').find('sura', index=str(surah_id))
        dat_english = soup_english.find('quran').find('sura', index=str(surah_id))
        for entry in dat_arabic.findAll('aya'):
            number = int(entry['index'])
            arabic = entry['text']# + create_end_of_ayat(number)
            english = dat_english.find('aya', index=str(number))['text']
            bismillah = entry.get('bismillah', '')
            ayat = Ayat(id, surah_id, number, arabic, english, bismillah)
            ayat.save()
            id += 1
    fil_arabic.close()
    fil_english.close()

def create_image(x):
    text = Ayat.get(x).arabic
    path = os.path.join(os.getcwd(), 'quranapp', 'static', 'image', '%s.jpeg' % x)
    os.system('pango-view --font="Scheherazade 28" --no-display --width=600 --output="%s" --text="%s"' % (path, text.encode('utf-8')))

def create_images():
    print 'Adding Images'
    for x in xrange(1, 6237):
        create_image(x)
        if x % 50 == 0:
            print 'Adding Image %s' % x

def main():
    ctx = quranapp.app.test_request_context()
    ctx.push()
    g.redis = redis.Redis(host='localhost', port=6379)
    add_surahs()
    add_ayats()
    create_images()
    ctx.pop()

if __name__ == '__main__':
    main()
