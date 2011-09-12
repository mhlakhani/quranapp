import quranapp
from quranapp.models import *
import os
from BeautifulSoup import BeautifulStoneSoup

def create_db():
    db.create_all()

def add_surahs():
    print 'Adding Surahs'
    fil = open(os.path.join(os.getcwd(), 'data', 'quran-data.xml'))
    soup = BeautifulStoneSoup(fil)
    entries = soup.find('quran').find('suras').findAll('sura')
    for entry in entries:
        id = int(entry['index'])
        name_arabic = entry['name']
        name_english = entry['ename']
        name_english_transliterated = entry['tname']
        num_ayas = entry['ayas']
        surah = Surah(id, name_arabic, name_english, name_english_transliterated, num_ayas)
        db.session.add(surah)
    db.session.commit()
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
    for surah_id in xrange(1,115):
        print 'Parsing Surah %s' % surah_id
        dat_arabic = soup_arabic.find('quran').find('sura', index=str(surah_id))
        dat_english = soup_english.find('quran').find('sura', index=str(surah_id))
        for entry in dat_arabic.findAll('aya'):
            number = int(entry['index'])
            arabic = entry['text']# + create_end_of_ayat(number)
            english = dat_english.find('aya', index=str(number))['text']
            bismillah = entry.get('bismillah', '')
            ayat = Ayat(surah_id, number, arabic, english, bismillah)
            db.session.add(ayat)
        db.session.commit()
    fil_arabic.close()
    fil_english.close()

def create_image(x):
    text = Ayat.query.get(x).arabic
    path = os.path.join(os.getcwd(), 'quranapp', 'static', 'image', '%s.png' % x)
    os.system('pango-view --font="Scheherazade 24" --no-display --width=500 --output="%s" --text="%s"' % (path, text.encode('utf-8')))

def create_images():
    print 'Adding Images'
    for x in xrange(1, 6237):
        create_image(x)
        if x % 50 == 0:
            print 'Adding Image %s' % x

def main():
    create_db()
    add_surahs()
    add_ayats()
    #create_images()

if __name__ == '__main__':
    main()
