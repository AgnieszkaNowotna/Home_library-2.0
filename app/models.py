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
    author = Author.query.filter_by(name = author_name, surname = author_surname).first()
    if author is None:
        author = Author(name = author_name, surname = author_surname)
        db.session.add(author)
        db.session.commit()
    return author

def create(data):
    data.pop('csrf_token')
    author = check_author(data)
    book = Books(author_id = author.id, 
                title = data['title'],
                release_year = data['release_year'],
                genre = data['genre'],
                description = data['description'],
                readed = data['readed'],
                cover = data['cover'],
                reviev = data['reviev'],
                score = data['rate'],
                )
    db.session.add(book)
    db.session.commit()

def update(book_id, data):
    book = Books.query.get(book_id)
    author = Author.query.get(book.author_id)
    book.author_id = author.id
    book.title = data['title']
    book.release_year = data['release_year']
    book.genre = data['genre']
    book.description = data['description']
    book.readed = data['readed']
    book.cover = data['cover']
    book.reviev = data['reviev']
    book.score = data['rate']
    db.session.add(book)
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

def create_data_to_update(book_id):
    position = Books.query.get(book_id)
    author = Author.query.get(position.author_id)
    author = f'{author.name} {author.surname}'
    data = {'title':position.title,
            'author':author,
            'release_year':position.release_year,
            'description':position.description,
            'readed':position.readed,
            'cover':position.cover,
            'reviev':position.reviev,
            'rate':position.score}
    return data