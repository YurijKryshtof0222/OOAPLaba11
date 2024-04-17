import concurrent.futures

from workua_vacancies_retriever import WorkUAVacanciesRetriever


def scrap_category(category_url):
    WorkUAVacanciesRetriever(category_url).traverse()


if __name__ == '__main__':
    base_url = 'https://www.work.ua'
    # Приклад списку URL для рубрики ІТ
    categories = [f'{base_url}/jobs-it/?page={i}' for i in range(1, 4)]
    # Приклад списку URL для рубрики Маркетинг
    categories.extend([f'{base_url}/jobs-sales/?page={i}' for i in range(1, 4)])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrap_category, categories)
