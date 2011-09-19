from fabric.api import local, env, cd, run, sudo, put
from fabric.context_managers import prefix
import os

try:
    import conf.fabfile
    HAVE_CONF = True
except Exception, ex:
    HAVE_CONF = False

env.hosts = ['mhlakhani.com']

def compile_css():
    local('lessc quranapp/static/css/quranapp.less --compress > quranapp/static/quranapp.css')

def compile_js():
    local('java -jar tools/compiler.jar --js quranapp/static/js/jquery.tablednd_0_5.js --js_output_file quranapp/static/quranapp.js')

def create_db():
    local('python create_db.py')

def run():
    local('python runserver.py')

def debug():
    os.environ['QURANAPP_CONFIG']="quranapp.config.DevelopmentConfig"

def deploy():
    if HAVE_CONF:
        conf.fabfile.deploy()
    else:
        print 'Please Create the Configure Fabfile'
