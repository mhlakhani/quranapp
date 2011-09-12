QuranApp
========

This is the code that powers http://quranapp.net

Development
-----------

### Required Packages

QuranApp requires a number of packages to run. The easiest way to install them is to use pip and virtualenv:

    virtualenv --no-site-packages --python=python2.7 env
    pip install -E env -r requirements.txt

To create the images of the ayats, pango-view is required. To install it on ubuntu use the following command:

    sudo apt-get install libpango1.0-dev

### Database Creation

QuranApp uses a number of data files from http://tanzil.net. The following files should be placed the data/ directory:

    quran-data.xml from http://tanzil.net/wiki/Quran_Metadata
    quran-uthmani.xml from http://tanzil.net/download
    en.hilali.xml from http://tanzil.net/trans/

Now setup the proper URL to the database in the quranapp/config.py file.
Then create the database using the following command:

    fab create_db
To setup the debug or mysql_dev databases, use 'debug' or 'mysql_dev' such as in:

    fab debug create_db

### Testing
To start the development server, run:

    fab run

Deployment
----------

### Compile and minify static files
QuranApp uses LESS-CSS and Google Closure Compiler. 
Install the LESS compiler using npm:

    npm install less
Download the Closure Compiler from http://closure-compiler.googlecode.com/files/compiler-latest.zip and save the .jar file to tools/compiler.jar

Then run the following commands to create the minified versions of static files:

    fab compile_css
    fab compile_js

### Pushing to Production
To push code to production, please make changes to the appropriate files in the conf/ directory, then run the following command:

    fab deploy

TODO: Create sample configuration files and place in conf/ directory. The current configuration needs to be modified to remove specfics before it can be used as a sample.
