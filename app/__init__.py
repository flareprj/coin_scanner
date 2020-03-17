from flask import Flask
from flask import render_template
from app.app import *
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():

    item = open_browser()

    print('--------------item------------------')
    print(item)

    createdb(item)

    return render_template('index.html', c=item)
    #return 'ok'


if __name__ == "__main__":
    app.run()
