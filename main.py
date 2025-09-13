from src.hh_api import get_employer_data, get_vacancies_by_employer
from src.db_utils import create_database, create_tables
from src.db_manager import DBManager

EMPLOYER_IDS = [1740, 9140614, 10914064, 11099814, 11550164, 11747243, 12021224, 5004072, 5775464, 4748227, 36227, 3172102, 11388989, 3643187, 90666985]  # 10 ID интересующих компаний

def fill_database():
    db = DBManager()
    for emp_id in EMPLOYER_IDS:
        employer = get_employer_data(emp_id)
        if not employer:
            continue

        with db.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO employers (name, url, open_vacancies)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (employer["name"], employer["alternate_url"], employer["open_vacancies"]))
            cur.execute("SELECT id FROM employers WHERE name = %s;", (employer["name"],))
            emp_db_id = cur.fetchone()[0]

            vacancies = get_vacancies_by_employer(emp_id)
            for vac in vacancies:
                if not vac.get("salary"):
                    continue
                salary_from = vac.get("salary", {}).get("from") or 0
                salary_to = vac.get("salary", {}).get("to") or 0

                currency = vac.get("salary", {}).get("currency") or "RUR"
                url = vac.get("alternate_url")

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

    db.conn.commit()
    db.conn.close()

if __name__ == "__main__":
    create_database()
    create_tables()
    fill_database()