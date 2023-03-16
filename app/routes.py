from flask import request, render_template, redirect, url_for, redirect
from app.forms import BookForm
from app.models import Books, Author, image_to_string, create, update, create_data_to_update
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
    

@app.route('/book/reviev/<int:book_id>', methods = ["GET", "POST"])   
def reviev(book_id):
    position = create_data_to_update(book_id)
    alternate_cover = position['cover']
    form = BookForm(data = position)
    if request.method == "POST":
        if form.validate_on_submit():
            data = image_to_string(form, (form.data), alternate_cover)
            update(book_id, data)
        return redirect(url_for('home'))

    return render_template("reviev.html", form = form,  book_id = book_id)
