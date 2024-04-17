import requests
from bs4 import BeautifulSoup


class WorkUAVacancyScrapper:
    def __init__(self, link):
        self.link = link
        self.offer_page = requests.get(self.link)
        self.soup = BeautifulSoup(self.offer_page.text, 'lxml')
        self.scrap_vacancy()

    def scrap_vacancy(self):
        self.job_title = self.soup.find('h1', id="h1-name").text
        self.company_name = self.extract_company_name()
        self.company_info = self.extract_company_info()
        self.location = self.extract_location()
        self.salary = self.extract_salary()
        self.description = self.extract_description()

    def extract_company_name(self):
        return (self.soup.find('span', class_="glyphicon glyphicon-company text-default glyphicon-large")
                .parent
                .find('span', class_="strong-500")).text

    def extract_company_info(self):
        result = (self.soup.find('span', class_="glyphicon glyphicon-company text-default glyphicon-large")
                  .parent
                  .find('span', class_="mt-xs text-default-7")).text

        return ' '.join(result.split())

    def extract_location(self):
        result = (self.soup.find('span', class_=["glyphicon glyphicon-map-marker text-default glyphicon-large",
                                                 "glyphicon glyphicon-remote text-default glyphicon-large"]))
        result = ' '.join(result.parent.text.split()) if result else "Не уточнено"
        return result

    def extract_salary(self):
        salary_elem = self.soup.find('span', class_="glyphicon glyphicon-hryvnia text-default glyphicon-large")
        if salary_elem:
            salary_text = salary_elem.parent.find('span', class_=["strong-500", "text-default-7"])
            return salary_text.text if salary_text else "Не вказано"
        return "Не вказано"

    def output_vacancy_info(self, file_name):
        print(self.link)
        print(self.job_title)
        print("Компанія: " + self.company_name)
        print("Зарплата: " + self.salary)
        print("Локація: " + self.location)
        print("Опис:\n " + self.description)

        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(f'Посилання: {self.link}\n')
            file.write(f'Назва вакансії: {self.job_title}\n')
            file.write(f'Компанія: {self.company_name}\n')
            file.write(f'Зарплата: {self.salary}\n')
            file.write(f'Локація: {self.location}\n\n')
            # file.write(f'Опис: {self.description}\n')

    def extract_description(self):
        return self.soup.find('div', id="job-description").text
