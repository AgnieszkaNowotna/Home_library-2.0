from flask import request, render_template, redirect, url_for, redirect
from app.forms import BookForm
from app.models import Books, Author, Status, image_to_string, create_position, update_position, delete_position, create_data_to_update
from app import app

@app.route('/book/')
def home():
    authors = Author
    book_status = Status
    books = Books.query.all()
    return render_template("book.html", books = books, authors = authors, book_status = book_status)

@app.route('/book/add/', methods = ["GET", "POST"])
def add():
    form = BookForm()
    error=""
    alternate_cover = 'brak_okładki.jpg'
    if request.method == 'POST':
        if form.validate_on_submit():
            data = image_to_string(form, (form.data), alternate_cover)
            create_position(data)
        return redirect(url_for('home'))
    return render_template("add.html", form = form, error = error)

@app.route('/book/reviev/<int:book_id>', methods = ["GET", "POST"])   
def reviev(book_id):
    position = create_data_to_update(book_id)
    alternate_cover = position['cover']
    form = BookForm(data = position)
    if request.method == "POST":
        if form.validate_on_submit():
            data = image_to_string(form, (form.data), alternate_cover)
            update_position(book_id, data)
        return redirect(url_for('home'))
    return render_template("reviev.html", form = form,  book_id = book_id)

@app.route("/book/delete/", methods = ["POST"])
def delete():
    data = request.form
    book_id = data.get('book_id')
    delete_position(book_id)
    return redirect(url_for('home'))
