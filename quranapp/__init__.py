from flask import Flask
import os
import sessions
app = Flask(__name__)
app.session_interface = sessions.RedisSessionInterface()

import quranapp.config
app.config.from_object('quranapp.config.DefaultConfig')
if os.environ.get('QURANAPP_CONFIG') is not None:
    app.config.from_object(os.environ['QURANAPP_CONFIG'])
if os.environ.get('QURANAPP_CONFIG_FILE') is not None:
    app.config.from_envvar('QURANAPP_CONFIG_FILE')

if not app.debug:
    import logging
    from logging import Formatter
    from logging.handlers import SMTPHandler, RotatingFileHandler
    file_handler = RotatingFileHandler(app.config['LOG_PATH'], maxBytes=1024*1024, backupCount=5)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
    logging.getLogger('xhtml2pdf').addHandler(file_handler)
    ADMINS = ['m.hasnain.lakhani@gmail.com']
    FROM = 'errors@quranapp.net'
    mail_handler = SMTPHandler(('smtp.gmail.com', 587), ADMINS[0], ADMINS, 'QuranApp Error', (FROM, app.config['EMAIL_PASSWORD']), secure=())
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
'''))
    app.logger.addHandler(mail_handler)

import quranapp.views
