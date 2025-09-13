import psycopg2

from config import DB_CONFIG


def create_database():
    try:
        # Подключение к системной БД (postgres)
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"],
            dbname="postgres",  # Всегда подключаемся к существующей БД
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Проверяем, существует ли БД
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_CONFIG['database']}';")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {DB_CONFIG['database']} ENCODING 'UTF8';")
            print(f"База данных '{DB_CONFIG['database']}' создана.")
        else:
            print(f"База данных '{DB_CONFIG['database']}' уже существует.")

        cur.close()
        conn.close()
    except Exception as e:
        print("Ошибка при работе с БД:", e)


def create_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url TEXT,
                open_vacancies INTEGER
            );
        """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(id),
                name VARCHAR(255) NOT NULL,
                salary_from NUMERIC,
                salary_to NUMERIC,
                currency VARCHAR(10),
                url TEXT
            );
        """
        )
    conn.commit()
    conn.close()
