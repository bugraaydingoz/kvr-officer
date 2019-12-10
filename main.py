import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from scraper import Scraper
from telegram_bot import TelegramBot

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
scheduler = BlockingScheduler()

INTERVAL = 5  # in minutes
scraper = Scraper()
bot = TelegramBot()


def get_message(appointments):
    logging.debug(appointments)
    free_appointments = []
    for date in appointments:
        value = appointments[date]
        if len(value) > 0:
            free_appointments.append(date)
            logging.info(date, value)

    if len(free_appointments) == 0:
        message = f"Nothing free - checking again in {INTERVAL} mins"
        logging.debug(message)
        # bot.send_message(message)  # ONLY FOR DEBUGGING

    else:
        url = "https://www46.muenchen.de/termin/index.php"
        message = f"I found these: {free_appointments}. Get your appointment here: {url}"
        logging.debug(message)
        bot.send_message(message)


def get_appointments():
    logging.info('Scraping appointments...')
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


@scheduler.scheduled_job(CronTrigger(minute=f"*/{INTERVAL}", hour='4-23', day='*', month='*', day_of_week='*'))
def check_appointment():
    logging.info('Starting scheduled job...')
    appointments = get_appointments()
    get_message(appointments)


@scheduler.scheduled_job(CronTrigger(minute="0", hour='7', day='*', month='*', day_of_week='*'))
def latest_appointment():
    logging.info('Starting scheduled job...')
    appointments = get_appointments()
    message = f"Daily Update\nLast KVR appointment: {max(appointments.keys())}"
    logging.debug(message)
    bot.send_message(message)


if __name__ == "__main__":
    logging.info('Initializing...')
    scheduler.add_job(check_appointment)
    scheduler.add_job(latest_appointment)
    scheduler.start()
