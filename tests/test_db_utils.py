import unittest
from unittest import mock
from src.db_utils import create_database, create_tables


class TestDBUtils(unittest.TestCase):

    @mock.patch("src.db_utils.psycopg2.connect")
    def test_create_database_exists(self, mock_connect):
        mock_cursor = mock.Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)

        create_database()

        # Проверяем, что SELECT был вызван с правильными параметрами
        mock_cursor.execute.assert_any_call("SELECT 1 FROM pg_database WHERE datname = %s;", ("hh_project",))

        # Проверяем, что CREATE DATABASE не был вызван
        execute_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
        self.assertNotIn("CREATE DATABASE", " ".join(execute_calls))

    @mock.patch("src.db_utils.psycopg2.connect")
    def test_create_database_not_exists(self, mock_connect):
        mock_cursor = mock.Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        create_database()

        mock_cursor.execute.assert_any_call("SELECT 1 FROM pg_database WHERE datname = %s;", ("hh_project",))
        mock_cursor.execute.assert_any_call("CREATE DATABASE hh_project ENCODING 'UTF8';")

    @mock.patch("src.db_utils.psycopg2.connect")
    def test_create_tables(self, mock_connect):
        # Создаем мок-курсор и настраиваем его как контекст-менеджер
        mock_cursor = mock.MagicMock()
        mock_cursor.__enter__.return_value = mock_cursor  # Курсор возвращает сам себя при входе в контекст
        mock_connect.return_value.cursor.return_value = mock_cursor

        create_tables()

        # Получаем все выполненные запросы
        execute_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
        print("Executed queries:", execute_calls)  # Для отладки

        # Проверяем, что оба запроса есть в списке
        self.assertTrue(any("CREATE TABLE IF NOT EXISTS employers" in query for query in execute_calls))
        self.assertTrue(any("CREATE TABLE IF NOT EXISTS vacancies" in query for query in execute_calls))


if __name__ == "__main__":
    unittest.main()
