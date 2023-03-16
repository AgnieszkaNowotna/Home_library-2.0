from flask import Flask, request, render_template, redirect, url_for, redirect
from app.forms import BookForm
from app.models import Books, Author, image_to_string, create
from app import app

@app.route('/book/')
def home():
    authors = Author
    books = Books.query.all()
    return render_template("book.html", books = books, authors = authors)

@app.route('/book/add/', methods = ["GET", "POST"])
def add():
    form = BookForm()
    error=""
    alternate_cover = 'brak_okładki.jpg'
    if request.method == 'POST':
        if form.validate_on_submit():
            data = image_to_string(form, (form.data), alternate_cover)
            create(data)
        return redirect(url_for('home'))
    
    return render_template("add.html", form = form, error = error)
"""
@app.route('/book/reviev/<string:book_title>', methods = ["GET", "POST"])   
def reviev(book_title):
    title = book_title
    book_id = book.get_id(title)
    position = book.get(book_id)
    alternate_cover = position['cover']
    form = BookForm(data = position)
    print(alternate_cover)

    if request.method == "POST":
        if form.validate_on_submit():
            data = book.image_to_string(form, app.config['UPLOAD_PATH'], (form.data), alternate_cover)
            book.update(book_id, data)
        return redirect(url_for('home'))

    return render_template("reviev.html", form = form,  book_title = book_title)
    """