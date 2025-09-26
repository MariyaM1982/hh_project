from src.hh_api import get_employer_data, get_vacancies_by_employer
from src.db_utils import create_database, create_tables
from src.db_manager import DBManager
from typing import List, Any, Optional, Dict


EMPLOYER_IDS: List[int] = [
    1740, 9140614, 10914064, 11099814, 11550164, 11747243, 12021224,
    5004072, 5775464, 4748227, 36227, 3172102, 11388989, 3643187
]  # 10 ID интересующих компаний

def fill_database() -> None:
    """
    Заполняет базу данных данными о компаниях и их вакансиях.

    Использует список EMPLOYER_IDS для получения информации о компаниях через API hh.ru.
    Вставляет данные в таблицы 'employers' и 'vacancies' в БД.
    Обрабатывает отсутствующие значения зарплат и пропускает некорректные данные.
    """
    db = DBManager()
    for emp_id in EMPLOYER_IDS:
        # Получение данных о компании
        employer: Optional[Dict[str, Any]] = get_employer_data(emp_id)
        if not employer:
            continue

        with db.conn.cursor() as cur:
            # Вставка данных компании
            cur.execute("""
                INSERT INTO employers (name, url, open_vacancies)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (employer["name"], employer["alternate_url"], employer["open_vacancies"]))

            # Получение ID компании из БД
            cur.execute("SELECT id FROM employers WHERE name = %s;", (employer["name"],))
            emp_db_id = cur.fetchone()[0]

            # Получение и обработка вакансий
            vacancies = get_vacancies_by_employer(emp_id)
            for vac in vacancies:
                if not vac.get("salary"):
                    continue

                # Обработка отсутствующих значений зарплаты
                salary_from = vac.get("salary", {}).get("from") or 0
                salary_to = vac.get("salary", {}).get("to") or 0
                currency = vac.get("salary", {}).get("currency") or "RUR"
                url = vac.get("alternate_url")

                # Вставка вакансии
                cur.execute("""
                    INSERT INTO vacancies (employer_id, name, salary_from, salary_to, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    emp_db_id,
                    vac.get("name"),
                    salary_from,
                    salary_to,
                    currency,
                    url
                ))

    # Сохранение изменений
    db.conn.commit()
    db.conn.close()

if __name__ == "__main__":
    """Точка входа для запуска скрипта."""
    create_database()
    create_tables()
    fill_database()