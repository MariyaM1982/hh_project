from src.db_manager import DBManager


def user_interface():
    """
    Интерфейс для взаимодействия с пользователем.

    Позволяет выбрать одно из следующих действий:
    1. Посмотреть компании и количество вакансий.
    2. Посмотреть все вакансии.
    3. Посмотреть среднюю зарплату по всем вакансиям.
    4. Посмотреть вакансии выше средней зарплаты.
    5. Найти вакансии по ключевому слову.

    В зависимости от выбора пользователя выполняются соответствующие методы класса DBManager.
    """
    db = DBManager()
    print("Выберите действие:")
    print("1. Посмотреть компании и количество вакансий")
    print("2. Посмотреть все вакансии")
    print("3. Средняя зарплата")
    print("4. Вакансии выше средней зарплаты")
    print("5. Вакансии по ключевому слову")

    choice = input("Введите номер: ")

    if choice == "1":
        for name, count in db.get_companies_and_vacancies_count():
            print(f"{name}: {count} вакансий")
    elif choice == "2":
        for company, title, from_salary, to_salary, url in db.get_all_vacancies():
            print(f"{company} - {title}, от {from_salary} до {to_salary} руб. [{url}]")
    elif choice == "3":
        print(f"Средняя зарплата: {db.get_avg_salary()} руб.")
    elif choice == "4":
        for company, title, from_salary, to_salary, url in db.get_vacancies_with_higher_salary():
            print(f"{company} - {title}, от {from_salary} до {to_salary} руб. [{url}]")
    elif choice == "5":
        keyword = input("Введите ключевое слово: ")
        for company, title, from_salary, to_salary, url in db.get_vacancies_with_keyword(keyword):
            print(f"{company} - {title}, от {from_salary} до {to_salary} руб. [{url}]")
    else:
        print("Неверный выбор.")


if __name__ == "__main__":
    user_interface()
