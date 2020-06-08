import schedule
from app.scanner import *


def index():
    schedule.every(30).seconds.do(open_browser)  # обновляем список монет через 30 секунд

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    index()
