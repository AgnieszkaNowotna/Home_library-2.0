from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,IntegerField, BooleanField, SelectField, FloatField, FileField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional
import datetime as dt

choices = ['-','Dramat','Komedia','Krminał','Thriller','Biograficzna', 'Historyczna','Romans','Sci-Fi','Fantastyka','Fantasy','Horror','Obyczajowa','Powieść dystopijna']
current_year = dt.datetime.now().strftime("%Y")

class BookForm(FlaskForm):
    title = StringField('Tytuł', validators = [DataRequired()])
    author = StringField('Autor', validators = [DataRequired()])
    additional_author = StringField('Autor', validators = [Optional()])
    release_year = IntegerField('Rok wydania', validators=[Optional(), NumberRange( min = 1000, max = int(current_year))])
    genre = SelectField('Gatunek', choices = choices, coerce = str, validators = [Optional()])
    description = TextAreaField('Opis', default = "-", validators = [Optional()])
    readed = BooleanField('Czy przeczytana', validators = [Optional()])
    cover = FileField('Okładka książki', validators = [Optional()])
    reviev = TextAreaField('Recenzja', default = "-", validators = [Optional()])
    rate = FloatField('Ocena', validators =[Optional(), NumberRange( min = 0, max = 10,)])
    avaliable = BooleanField('Czy dostępna', default = "True", validators = [Optional()])
    date_of_hire = DateField('Data wypożyczenia',format='%Y-%m-%d', validators = [Optional()])
    date_of_handover = DateField('Data oddania',format='%Y-%m-%d' , validators = [Optional()])
