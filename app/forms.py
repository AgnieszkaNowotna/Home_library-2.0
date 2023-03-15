from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,IntegerField, BooleanField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, NumberRange, Optional
import datetime as dt

choices = ['-','Dramat','Komedia','Krminał','Thriller','Biograficzna', 'Historyczna','Romans','Sci-Fi','Fantastyka','Fantasy','Horror','Obyczajowa','Powieść dystopijna']
current_year = dt.datetime.now().strftime("%Y")

class BookForm(FlaskForm):
    title = StringField('Tytuł', validators = [DataRequired()])
    author = StringField('Autor', validators = [DataRequired()])
    release_year = IntegerField('Data wydania', validators=[Optional(), NumberRange( min = 1000, max = int(current_year))])
    genre = SelectField('Gatunek', choices = choices, coerce = str, validators = [Optional()])
    description = TextAreaField('Opis', default = "-", validators = [Optional()])
    readed = BooleanField('Czy przeczytana', validators = [Optional()])
    cover = FileField('Okładka książki', validators = [Optional()])
    reviev = TextAreaField('Recenzja', default = "-", validators = [Optional()])
    rate = IntegerField('Ocena', validators =[Optional(), NumberRange( min = 0, max = 10,)])