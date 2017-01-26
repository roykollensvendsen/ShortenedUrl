"""
Routes and views for the flask application.
"""

from baseconv import BaseConverter
from datetime import datetime
from flask import render_template, url_for, request, redirect
from ShortenedUrl import app
from ShortenedUrl.database import db_session
from ShortenedUrl.models import UrlEntry
from sqlalchemy import exc
from sqlalchemy.sql import exists
from urllib.parse import urlparse


bc = BaseConverter('abcdefghijklmnopqrstuvwxyz')

def id2url(id):
    return bc.encode(str(id))

def url2id(url):
    return bc.decode(url)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/s', methods=['POST'])
def shorten_url():
    url=request.form['url']
    url=urlparse(url)
    if url.scheme == '' or url.netloc == '':
        return 'Enter a full URL with scheme and netloc'
    if url.path[-1:] == '/':
        url = url._replace(path=url.path.rstrip('/'))
    url=url.geturl()
    url_entry = UrlEntry(url)
    db_session.add(url_entry)
    try:
        db_session.commit()
    except:
        db_session.rollback()
        if db_session.query(exists().where(UrlEntry.url == url)).scalar():
             url_entry = UrlEntry.query.filter_by(url=url).first()
    short_url='http://%s/%s' % ("my-site.no", id2url(url_entry.id))
    return render_template('shortened_url.html', url=url, short_url=short_url)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/<path:path>')
def catch_all(path):
    return redirect(UrlEntry.query.get(url2id(path)).url)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
