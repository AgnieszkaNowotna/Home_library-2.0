from app import db
from werkzeug.utils import secure_filename
import os
import json

class Book:
    def __init__(self):
        try:
            with open ("books.json", "r", encoding = "UTF-8") as f:
                self.library = json.load(f)
        except FileNotFoundError:
            self.library = []

    def all(self):
        return self.library
    
    def get_id(self, title):
        id = 0
        for position in self.library:
            if position['title'] == title:
                return id
            else:
                id +=1

    def get(self,id):
        return self.library[id]
    
    def create(self, data):
        data.pop('csrf_token')
        self.library.append(data)

    def save_all(self):
        with open("books.json", "w", encoding="UTF-8")as f:
            json.dump(self.library, f, ensure_ascii=False)

    def update(self, id, data):
        data.pop('csrf_token')
        self.library[id] = data
        self.save_all()

    def image_to_string(self, form, path, data, alternate_cover):
        try:
            f = form.cover.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(path, filename))
            cover = str(data['cover'])
            replace_name = cover.split(" ")
            data['cover'] = replace_name[1].replace('"','')
            return data
        except FileNotFoundError:
            data['cover'] = alternate_cover
            return data

book = Book()

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