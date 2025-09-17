import unittest
from unittest import mock
from src.hh_api import get_employer_data, get_vacancies_by_employer

class TestHHAPI(unittest.TestCase):

    @mock.patch('hh_api.requests.get')
    def test_get_employer_data_success(self, mock_get):
        # Подготавливаем мок-ответ
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1740,
            "name": "Яндекс",
            "alternate_url": "https://hh.ru/employer/1740",
            "open_vacancies": 50
        }
        mock_get.return_value = mock_response

        result = get_employer_data(1740)
        self.assertEqual(result["name"], "Яндекс")
        self.assertEqual(result["open_vacancies"], 50)

    @mock.patch('hh_api.requests.get')
    def test_get_employer_data_not_found(self, mock_get):
        # Подготавливаем мок-ответ
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.text = '{"description":"Not Found"}'
        mock_get.return_value = mock_response

        result = get_employer_data(999999)
        self.assertIsNone(result)

    @mock.patch('hh_api.requests.get')
    def test_get_vacancies_by_employer_success(self, mock_get):
        # Подготавливаем мок-ответ
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python разработчик",
                    "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
                    "alternate_url": "https://hh.ru/vacancy/123"
                },
                {
                    "name": "Java разработчик",
                    "salary": {"from": 100000, "to": 160000, "currency": "RUR"},
                    "alternate_url": "https://hh.ru/vacancy/456"
                }
            ]
        }
        mock_get.return_value = mock_response

        vacancies = get_vacancies_by_employer(1740)
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0]["name"], "Python разработчик")

    @mock.patch('hh_api.requests.get')
    def test_get_vacancies_by_employer_not_found(self, mock_get):
        # Подготавливаем мок-ответ
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.text = '{"description":"Not Found"}'
        mock_get.return_value = mock_response

        vacancies = get_vacancies_by_employer(999999)
        self.assertEqual(len(vacancies), 0)

if __name__ == "__main__":
    unittest.main()