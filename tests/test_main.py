import unittest
from unittest import mock
from main import fill_database


class TestMain(unittest.TestCase):

    @mock.patch('src.main.get_employer_data', return_value=None)
    @mock.patch('src.main.get_vacancies_by_employer', return_value=[])
    def test_fill_database_no_data(self, mock_vacancies, mock_employer):
        fill_database()
        # Здесь можно проверить логи или вставить assert-ы по необходимости

    @mock.patch('src.main.get_employer_data', return_value={
        "id": 1740,
        "name": "Яндекс",
        "alternate_url": "https://hh.ru/employer/1740",
        "open_vacancies": 50
    })
    @mock.patch('src.main.get_vacancies_by_employer', return_value=[
        {
            "name": "Python разработчик",
            "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/123"
        }
    ])
    def test_fill_database_success(self, mock_vacancies, mock_employer):
        fill_database()
        # Здесь можно проверить логи или вставить assert-ы по необходимости


if __name__ == "__main__":
    unittest.main()