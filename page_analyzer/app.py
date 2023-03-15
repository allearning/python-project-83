import os
from flask import Flask, flash, get_flashed_messages, redirect, request, render_template, url_for
from page_analyzer.url_utils import validate_url, cut_netloc
from dotenv import load_dotenv

from page_analyzer.seopage import SEOPage
from page_analyzer.connector import Connector
from page_analyzer import db as database


load_dotenv()
app = Flask(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')
app.secret_key = os.getenv('SECRET_KEY')
app.config.from_mapping(DATABASE=DATABASE_URL)
with app.app_context():
    database.init_app(app)


@app.route('/')
def get_index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.get('/urls/<page_id>')
def get_url_page(page_id):
    db = Connector(database.get_db())
    messages = get_flashed_messages(with_categories=True)
    page = db.get_page_by_id(page_id)
    if not page:
        return render_template('notfound.html', messages=messages), 404
    page.checks = db.get_checks_for_page(page.page_id)
    return render_template('urls/index.html', page=page, messages=messages)


@app.post('/urls')
def post_add_page():
    #check page address
    #if bad redirect to '/' with error message
    #if not in db
    #   add to db
    #redirect to page of page
    db = Connector(database.get_db())
    address = request.form.get('url')
    errors = validate_url(address)
    if errors:
        for error in errors:
            flash(error, category='alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages, url_text=address), 402

    address = cut_netloc(address)
    page = db.get_page(address)
    if page:
        flash("Страница уже существует", category='alert-info')
        return redirect(url_for('get_url_page', page_id=page.page_id), code=302)

    db.add_page(SEOPage(address))
    page = db.get_page(address)
    flash("Страница успешно добавлена", category='alert-success')
    return redirect(url_for('get_url_page', page_id=page.page_id), code=302)


@app.get('/urls')
def get_urls():
    db = Connector(database.get_db())
    messages = get_flashed_messages(with_categories=True)
    pages = db.get_pages()
    for page in pages:
        page.checks.append(db.get_last_check(page.page_id))
    return render_template('urls/summary.html', pages=pages, messages=messages)


@app.post('/urls/<page_id>/checks')
def post_check_page(page_id):
    db = Connector(database.get_db())
    page = db.get_page_by_id(page_id)
    try:
        new_check = page.check()
        db.add_check(new_check)
        flash('Страница успешно проверена', category='alert-success')
    except Exception as e:
        print(e)
        flash('Произошла ошибка при проверке', category='alert-danger')
    return redirect(url_for('get_url_page', page_id=page_id), code=302)
