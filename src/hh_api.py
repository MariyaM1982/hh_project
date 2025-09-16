import logging

import requests

logging.basicConfig(level=logging.INFO)

HH_API_URL = "https://api.hh.ru/employers"


def get_employer_data(employer_id):
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Ошибка получения данных о компании {employer_id}: {response.text}")
        return None
    return response.json()


def get_vacancies_by_employer(employer_id):
    url = "https://api.hh.ru/vacancies"
    params = {"employer_id": employer_id, "per_page": 100}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        logging.error(f"Ошибка получения вакансий для {employer_id}: {response.text}")
        return []
    return response.json()["items"]  #
