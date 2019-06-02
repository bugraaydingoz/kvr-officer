from scraper import Scraper
from telegram_bot import TelegramBot
import schedule
import time

MINUTES = 10
scraper = Scraper()
bot = TelegramBot()


def get_message(appointments):
    print(appointments)
    free_appointments = []
    message = ""
    send_message = False
    for date in appointments:
        value = appointments[date]
        if len(value) > 0:
            free_appointments.append(date)
            print(date, value)

    if len(free_appointments) == 0:
        message = f"Unfortunately I couldn't find any free appointment :( but I will keep you updated in {MINUTES} mins."
        send_message = False
        print(message)

    else:
        url = "https://www46.muenchen.de/termin/index.php"
        message = "I found these: {free_appointments}. Get your appointment here: {url}"
        send_message = True
        print(message)

    return message, send_message


def get_appointments():
    counter = 0
    while counter < 5:
        try:
            appointments = scraper.get_appointments()
            if type(appointments) is dict:
                return appointments

        except Exception as e:
            print(e)
            pass

        counter += 1


def job():
    print()
    print('Cron job running...')
    appointments = get_appointments()
    message, send_message = get_message(appointments)
    if send_message:
        bot.send_message(message)


job()
schedule.every(MINUTES).minutes.do(job)
while 1:
    schedule.run_pending()
    time.sleep(1)
