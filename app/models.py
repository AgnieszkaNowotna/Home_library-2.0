from app import db
from config import BASE_DIR
from werkzeug.utils import secure_filename
import os

author_of_book = db.Table('author_of_book',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')))

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), index=True, nullable = False)
    surname = db.Column(db.String(200), index=True, nullable = False)
    book = db.relationship("Books", secondary = author_of_book, backref = "author")

class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), index=True, nullable = False)
    release_year = db.Column(db.Integer)
    genre = db.Column(db.String(200))
    description = db.Column(db.Text)
    readed = db.Column(db.Boolean, nullable = False)
    cover = db.Column(db.Text)
    reviev = db.Column(db.Text)
    rate = db.Column(db.Float)
    status_id = db.relationship("Status", backref = "book")

class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    avaliable = db.Column(db.Boolean)
    date_of_hire = db.Column(db.Date)
    date_of_handover = db.Column (db.Date)

def create_position(data):
    data.pop('csrf_token')
    book = Books(
                title = data['title'],
                release_year = data['release_year'],
                genre = data['genre'],
                description = data['description'],
                readed = data['readed'],
                cover = data['cover'],
                reviev = data['reviev'],
                rate = data['rate'],
                )
    db.session.add(book)
    db.session.commit()
    book_status = Status(
                        book_id = book.id,
                        avaliable = data['avaliable'],
                        date_of_hire = data['date_of_hire'],
                        date_of_handover = data['date_of_handover']
                        )
    db.session.add(book_status)
    author = create_author(data,'author')
    additional_author = create_author(data,'additional_author')
    author.book.append(book)
    if additional_author is not None:
        additional_author.book.append(book)
    db.session.commit()

def update_position(book_id, data):
    book = Books.query.get(book_id)
    book.title = data['title']
    book.release_year = data['release_year']
    if data['genre'] !="-":
        book.genre = data['genre']
    else:
        pass
    book.description = data['description']
    book.readed = data['readed']
    book.cover = data['cover']
    book.reviev = data['reviev']
    book.rate = data['rate']

    create_author(data, 'author')
    create_author(data, 'additional_author')

    stat = Status.query.filter_by(book_id = book_id).first()
    stat.avaliable = data['avaliable']
    stat.date_of_hire = data['date_of_hire']
    stat.date_of_handover = data['date_of_handover']
    
    db.session.add_all([book, stat])
    db.session.commit()

def delete_position(book_id):
    book = Books.query.get(book_id)
    stat = Status.query.filter_by(book_id=book_id).first()
    print(stat)
    author = book.author[0]
    if len(db.session.query(author_of_book).filter_by(author_id = author.id).all()) < 2:
        db.session.delete(author)
    if len(book.author)>1:
        additional_author = book.author[1]
        if len(db.session.query(author_of_book).filter_by(author_id = additional_author.id).all()) < 2:
            db.session.delete(additional_author)
    db.session.delete(stat)
    db.session.delete(book)
    db.session.commit()

def create_author(data, field):
    if data[field] !="":
        name_surname = data[field].split(" ")
        author_name = name_surname[0].capitalize()
        author_surname = " ".join(name_surname[1:]).title()
        author = Author.query.filter_by(name = author_name, surname = author_surname).first()
        if author is None:
            author = Author(name = author_name, surname = author_surname)
            db.session.add(author)
        return author

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
    author = position.author[0]
    author = f'{author.name} {author.surname}'
    if len(position.author)>1:
        additional_author = position.author[1]
        additional_author = f'{additional_author.name} {additional_author.surname}'
    else:
        additional_author = ""
    stat = Status.query.filter_by(book_id = book_id).first()
    data = {'title':position.title,
            'author':author,
            'additional_author':additional_author,
            'release_year':position.release_year,
            'description':position.description,
            'readed':position.readed,
            'cover':position.cover,
            'reviev':position.reviev,
            'rate':position.rate,
            'avaliable':stat.avaliable,
            'date_of_hire':stat.date_of_hire,
            'date_of_handover':stat.date_of_handover
            }
    return data