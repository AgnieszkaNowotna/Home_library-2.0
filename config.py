from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "kdfjkldsfl"
app.config['UPLOAD_PATH'] = os.path.join(app.static_folder, 'covers')
