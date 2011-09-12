from quranapp import app
from quranapp.models import db, Ayat, Surah
from flask import g, request, render_template, session, redirect, url_for, send_file
from xhtml2pdf import pisa
import logging, sys, os

try:
    import cStringIO as StringIO
except Exception:
    import StringIO #FIXME: log this

def int_or_none(var, method='POST'):
    attr = {'POST':'form', 'GET':'args'}
    tmp = getattr(request, attr[method]).get(var)
    try:
        tmp = int(tmp)
        return tmp
    except Exception, ex:
        # FIXME: log something here
        return None

@app.before_request
def before_request():
    g.debug = app.debug

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/browse/', defaults={'surah_no': 1, 'page': 1}, methods=['GET', 'POST'])
@app.route('/browse/<int:surah_no>/<int:page>', methods=['GET', 'POST'])
def browse(surah_no, page):
    post_ayat = None
    per_page = 10
    selected_ayats = [] # FIXME: start using ordered sets here
    if session.get('selected') is not None and session.get('selected') != '':
        selected_ayats = [int(x) for x in session['selected'].split(':')]
    if request.method == 'POST':
        ayat = int_or_none('select')
        post_surah = int_or_none('surah_no')
        post_ayat = int_or_none('ayat_no')
        if ayat is not None:
            if session.new:
                session['selected'] = ''
            if ayat in selected_ayats:
                selected_ayats = [x for x in selected_ayats if x != ayat]
            else:
                selected_ayats.append(ayat)
            session['selected'] = ':'.join([str(x) for x in selected_ayats])
        if post_surah is not None and 1 <= post_surah <= 114:
            surah_no = post_surah
    surah = Surah.query.get_or_404(surah_no)
    surah_name = surah.name_english_transliterated
    surah_list = Surah.query.all()
    if post_ayat is not None and post_ayat <= surah.num_ayats and post_ayat > 0:
        page = (post_ayat - 1) / per_page + 1
    pagination = surah.ayats.paginate(page=page, per_page=per_page)
    return render_template('browse.html', **locals())

@app.route('/review/', methods=['GET', 'POST'])
def review():
    choices = ['include_arabic', 'include_english']
    selected_ayats = []
    if session.get('selected') is not None and session.get('selected') != '':
        selected_ayats = [int(x) for x in session['selected'].split(':')]
    for key in choices:
        if session.get(key) is None:
            session[key] = True
    settings_tab = request.args.get('settings_tab', 'content')
    if settings_tab not in ['content', 'notes']:
        settings_tab = 'content'
    if request.method == 'POST':
        if settings_tab == 'content' and request.form.get('deselect') is None and request.form.get('ordering') is None:
            for key in choices:
                session[key] = key in request.form.keys()
            if all([session[key] == False for key in choices]):
                error_message = 'Please include English or Arabic (or both).'
                for key in choices:
                    session[key] = True
        if settings_tab == 'notes' and request.form.get('deselect') is None and request.form.get('ordering') is None:
            session['notes'] = request.form.get('notes')
        if request.form.get('ordering') is not None and request.form.get('ordering') != '':
            ayats = request.form.get('ordering').split('&duas[]=')
            ayats = [x for x in ayats if x.isdigit()]
            selected_ayats = map(int, ayats)
            session['selected'] = ':'.join([str(x) for x in selected_ayats])
        ayat = int_or_none('deselect')
        if ayat is not None:
            selected_ayats = [x for x in selected_ayats if x != ayat]
            session['selected'] = ':'.join([str(x) for x in selected_ayats])
    locals().update(session)
    items = Ayat.query.filter(Ayat.id.in_(selected_ayats)).all()
    ordering = dict([(v,k) for (k,v) in enumerate(selected_ayats)])
    items.sort(key = lambda x: ordering[x.id])
    return render_template('review.html', **locals())

@app.route('/create/<string:format>/', methods=['POST'])
def create(format):
    selected_ayats = []
    if session.get('selected') is not None and session.get('selected') != '':
        selected_ayats = [int(x) for x in session['selected'].split(':')]
    locals().update(session)
    items = Ayat.query.filter(Ayat.id.in_(selected_ayats)).all()
    ordering = dict([(v,k) for (k,v) in enumerate(selected_ayats)])
    items.sort(key = lambda x: ordering[x.id])
    if format not in ['pdf', 'html']:
        format = 'html'
    out_file = os.path.join(os.getcwd(), 'out.%s' % format)
    input = render_template('output_%s.html' % format, **locals())
    output = StringIO.StringIO()
    if format == 'html':
        print>>output, input.encode('utf-8')
    elif format == 'pdf':
        result = pisa.pisaDocument(input, output)
    output.seek(0)
    return send_file(output, as_attachment=True, attachment_filename='download.%s' % format)
