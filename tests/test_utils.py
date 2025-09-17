import unittest
from unittest import mock
from src.utils import user_interface


class TestUtils(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['1'])
    @mock.patch('src.utils.DBManager')
    def test_user_interface_1(self, mock_db, mock_input):
        db_instance = mock_db.return_value
        db_instance.get_companies_and_vacancies_count.return_value = [('Яндекс', 50)]

        user_interface()

        db_instance.get_companies_and_vacancies_count.assert_called_once()

    @mock.patch('builtins.input', side_effect=['2'])
    @mock.patch('src.utils.DBManager')
    def test_user_interface_2(self, mock_db, mock_input):
        db_instance = mock_db.return_value
        db_instance.get_all_vacancies.return_value = [('Яндекс', 'Python разработчик', 120000, 180000, 'url')]

        user_interface()

        db_instance.get_all_vacancies.assert_called_once()

    @mock.patch('builtins.input', side_effect=['3'])
    @mock.patch('src.utils.DBManager')
    def test_user_interface_3(self, mock_db, mock_input):
        db_instance = mock_db.return_value
        db_instance.get_avg_salary.return_value = 140000

        user_interface()

        db_instance.get_avg_salary.assert_called_once()

    @mock.patch('builtins.input', side_effect=['4'])
    @mock.patch('src.utils.DBManager')
    def test_user_interface_4(self, mock_db, mock_input):
        db_instance = mock_db.return_value
        db_instance.get_vacancies_with_higher_salary.return_value = [('Яндекс', 'Python разработчик', 120000, 180000, 'url')]

        user_interface()

        db_instance.get_vacancies_with_higher_salary.assert_called_once()

    @mock.patch('builtins.input', side_effect=['5', 'Python'])
    @mock.patch('src.utils.DBManager')
    def test_user_interface_5(self, mock_db, mock_input):
        db_instance = mock_db.return_value
        db_instance.get_vacancies_with_keyword.return_value = [('Яндекс', 'Python разработчик', 120000, 180000, 'url')]

        user_interface()

        db_instance.get_vacancies_with_keyword.assert_called_once_with("Python")


if __name__ == "__main__":
    unittest.main()