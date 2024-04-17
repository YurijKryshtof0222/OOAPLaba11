import re

import requests
from bs4 import BeautifulSoup

from workua_vacancy_scrapper import WorkUAVacancyScrapper


def trim_url(url):
    pattern = r'(jobs-it|jobs-sales)/\?page=\d+'
    match = re.search(pattern, url)
    if match:
        return match.group(0).replace("/?page=", "")
    else:
        return None


class WorkUAVacanciesRetriever:
    base_url = 'https://www.work.ua'

    def __init__(self, url):
        self.url = url
        self.file_name = trim_url(url) + ".txt"
        self.traverse_page = requests.get(url)
        self.soup = BeautifulSoup(self.traverse_page.text, 'html.parser')

    def traverse(self):
        jobs_list_div = self.soup.find("div", id="pjax-jobs-list")
        jobs_list = jobs_list_div.find_all("div", class_="card card-hover card-search card-visited wordwrap job-link "
                                                         "js-job-link-blank js-hot-block")
        for job_offer_elem in jobs_list:
            job_header = job_offer_elem.find("h2", class_="cut-top cut-bottom")
            offer_link = WorkUAVacanciesRetriever.base_url + job_header.find("a", href=True)['href']

            job_offer = WorkUAVacancyScrapper(offer_link)
            job_offer.output_vacancy_info(file_name=self.file_name)
