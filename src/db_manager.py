import psycopg2
from typing import List, Tuple
from config import DB_CONFIG
from decimal import Decimal


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self) -> List[Tuple]:
        """
        Возвращает список всех компаний и количество вакансий у каждой компании.

        Returns:
            List[Tuple]: Список кортежей (company_name, vacancy_count).
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, COUNT(v.id)
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.name;
            """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple]:
        """
        Возвращает список всех вакансий с информацией о компании.

        Returns:
            List[Tuple]: Список кортежей (company_name, vacancy_name, salary_from, salary_to, url).
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id;
            """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Возвращает среднюю зарплату по всем вакансиям.

        Returns:
            float: Средняя зарплата.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_from + salary_to) / 2)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            """
            )
            result = cur.fetchone()[0]
            # Конвертируем Decimal в float
            avg_salary = float(result or 0)
            return round(avg_salary, 2)

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """
        Возвращает список вакансий, у которых зарплата выше средней.

        Returns:
            List[Tuple]: Список кортежей (company_name, vacancy_name, salary_from, salary_to, url).
        """
        with self.conn.cursor() as cur:
            avg_salary = self.get_avg_salary()
            cur.execute(
                """
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE (v.salary_from + v.salary_to) / 2 > %s;
            """,
                (avg_salary,),
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """
        Возвращает список вакансий, содержащих указанное ключевое слово.

        Args:
            keyword (str): Ключевое слово для поиска.

        Returns:
            List[Tuple]: Список кортежей (company_name, vacancy_name, salary_from, salary_to, url).
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE v.name ILIKE %s;
            """,
                (f"%{keyword}%",),
            )
            return cur.fetchall()
