from flask import Flask
import os
app = Flask(__name__)

app.url_map.strict_slashes = False
_dir = os.path.dirname(os.path.abspath(__file__))
app.template_folder = os.path.join(_dir, "template")
app.static_folder = os.path.join(_dir, "static")
app.config['UPLOAD_FOLDER'] = os.path.join(_dir, "upload")