from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.__static_folder = 'STATIC_FOLDER_PATH'

from app import general

@app.context_processor
def current_year():
    return {'current_year': datetime.utcnow().year}
