import json
import os
import re
from urllib.parse import quote

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests import Session

load_dotenv(dotenv_path='.env')
appointment = quote(os.environ['APPOINTMENT_TYPE'])
appointment_code = str(os.environ['APPOINTMENT_CODE'])
num = os.environ.get('APPOINTMENT_QUANTITY', 1)


class Scraper:

    def __init__(self):
        self.session = Session()

        # Request params
        self.url = "https://www46.muenchen.de/termin/index.php"
        self.querystring = {"cts": appointment_code}
        self.payload = f"step=WEB_APPOINT_SEARCH_BY_CASETYPES&{appointment}={num}"
        self.headers = {
            'Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'Origin': "https://www46.muenchen.de",
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept-Encoding': "gzip, deflate, br",
            'cookie': "PHPSESSID=ma0117fsbng4icvfn92fn7umh6",
            'Host': "www46.muenchen.de",
            'cache-control': "no-cache"
        }

    def get_appointments(self):
        original_response = self.__get_response_from_website()
        return self.__scrape_html(html=original_response)

    def __get_response_from_website(self):
        # Get session id
        self.session.request("GET", self.url)

        # Get real data
        response = self.session.request(
            "POST", self.url, data=self.payload, headers=self.headers, params=self.querystring)
        return response.text

    def __scrape_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        script_tag = soup.find_all('script')[3].string
        regex = r'var jsonAppoints = (.*?);'
        appointments_text = self.__find_json_object(
            regex=regex, text=script_tag)

        appointments = json.loads(appointments_text)
        return appointments["Termin Wartezone SCIF"]["appoints"]

    @staticmethod
    def __find_json_object(regex, text):
        match = re.search(regex, text)
        appointments = str(match.groups()[0])
        appointments = appointments[1:len(appointments) - 1]
        return appointments
