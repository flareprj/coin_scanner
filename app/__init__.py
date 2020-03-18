import schedule
from flask import Flask
from flask import render_template
from app.app import *
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    #conn = sqlite3.connect("coins.db")
    #cursor = conn.cursor()

    #n = cursor.execute("SELECT COUNT(*) FROM setcoins")
    #values = n.fetchone()

    #item = open_browser()

    schedule.every(20).seconds.do(open_browser)

    while True:
        schedule.run_pending()


    # while values[0] < 4:  # сколько раз будем обновлять часть данных
    #     schedule.run_pending()
    #     n = cursor.execute("SELECT COUNT(*) FROM setcoins")
    #     values = n.fetchone()
    #     print(values[0])

    #return render_template('index.html', c=item)
    #return 'ok'


if __name__ == "__main__":
    app.run()
