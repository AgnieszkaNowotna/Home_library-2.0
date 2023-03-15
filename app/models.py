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

