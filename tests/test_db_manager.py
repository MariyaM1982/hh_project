import unittest
from src.db_manager import DBManager
from src.db_utils import create_database, create_tables


class TestDBManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Выполняется один раз перед запуском всех тестов."""
        create_database()
        create_tables()

    def test_get_companies_and_vacancies_count(self):
        db = DBManager()
        result = db.get_companies_and_vacancies_count()
        self.assertIsInstance(result, list)
        for item in result:
            self.assertEqual(len(item), 2)

    def test_get_all_vacancies(self):
        db = DBManager()
        result = db.get_all_vacancies()
        self.assertIsInstance(result, list)
        for item in result:
            self.assertEqual(len(item), 5)

    def test_get_avg_salary(self):
        db = DBManager()
        result = db.get_avg_salary()
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_get_vacancies_with_higher_salary(self):
        db = DBManager()
        result = db.get_vacancies_with_higher_salary()
        self.assertIsInstance(result, list)
        for item in result:
            self.assertEqual(len(item), 5)

    def test_get_vacancies_with_keyword(self):
        db = DBManager()
        result = db.get_vacancies_with_keyword("разработчик")
        self.assertIsInstance(result, list)
        for item in result:
            self.assertEqual(len(item), 5)


if __name__ == "__main__":
    unittest.main()
