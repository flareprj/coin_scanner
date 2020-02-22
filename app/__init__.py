from flask import Flask
from flask import render_template
from app.app import *

app = Flask(__name__)


@app.route('/')
def index():

    item, nested = open_browser()
    c = np.concatenate((item, nested), axis=1)

    print(c)
    print('----------------------------------')

    return render_template('index.html', c=c)


if __name__ == "__main__":
    app.run()
