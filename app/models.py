from app import db
from config import BASE_DIR
from werkzeug.utils import secure_filename
import os

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), index=True, nullable = False)
    surname = db.Column(db.String(200), index=True, nullable = False)
    author_id = db.relationship("Books", backref = "author", lazy="dynamic")

class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(200), index=True, nullable = False)
    release_year = db.Column(db.Integer)
    genre = db.Column(db.String(200))
    description = db.Column(db.Text)
    readed = db.Column(db.Boolean, nullable = False)
    cover = db.Column(db.Text)
    reviev = db.Column(db.Text)
    score = db.Column(db.Float)
    status_id = db.relationship("Status", backref = "book")

class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    avaliable = db.Column(db.Boolean)
    date_of_hire = db.Column(db.Date)
    end_of_handover = db.Column (db.Date)

def check_author(data):
    name_surname = data['author'].split(" ")
    author_name = name_surname[0].capitalize()
    author_surname = " ".join(name_surname[1:]).title()
    new_author = Author.query.filter_by(name = author_name, surname = author_surname).first()
    if new_author is None:
        new_author = Author(name = author_name, surname = author_surname)
        db.session.add(new_author)
        db.session.commit()
    return new_author

def create(data):
    data.pop('csrf_token')
    new_author = check_author(data)
    new_book = Books(author_id = new_author.id, 
                    title = data['title'],
                    release_year = data['release_year'],
                    genre = data['genre'],
                    description = data['description'],
                    readed = data['readed'],
                    cover = data['cover'],
                    reviev = data['reviev'],
                    score = data['rate'],
                    )
    db.session.add(new_book)
    db.session.commit()

def image_to_string(form, data, alternate_cover):
    try:
        f = form.cover.data
        filename = secure_filename(f.filename)
        path = os.path.join(BASE_DIR, 'app\\static\\covers', filename)
        f.save(path)
        cover = str(data['cover'])
        replace_name = cover.split(" ")
        data['cover'] = replace_name[1].replace("'","")
        return data
    except FileNotFoundError:
        data['cover'] = alternate_cover
        return data
