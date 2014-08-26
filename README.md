QuranApp
========

This is the code that powers http://quranapp.net

Development
-----------

### Database Creation

QuranApp uses a number of data files from http://tanzil.net. The following files should be placed the data/ directory:

    quran-data.xml from http://tanzil.net/wiki/Quran_Metadata
    quran-uthmani.xml from http://tanzil.net/download
    en.hilali.xml from http://tanzil.net/trans/

Then create the database using the following command:

    python create_db.py

## Images

QuranApp requires some static images to be created for PDF generation. The easiest way to do that is to:

1. Generate an HTML file containing every single aya, in order
2. Serve this file at some URL
3. Use casperjs with data/images.js to screenshot and generate images appropriately

These images should then be copied to static/image/

Deployment
----------

### Pushing to Production

Deployment just requires pushing the index.html file and the static/ directory to a publicly accessible directory.
