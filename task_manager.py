# task_manager.py
# Главный модуль: меню и вызов отчётов.
# Никаких импортов, кроме собственных модулей.

from family_task import DateTime, create_base, save_to_file, load_from_file
from reports import report_1_last_n_days, report_2_failed_by_member, report_3_in_progress


def print_tasks(task_list: list):
    """Выводит список задач в виде таблицы."""
    if not task_list:
        print("(Список пуст)")
        return

    header = (f"{'Дата выдачи':<22} {'Дедлайн':<22} "
              f"{'Исполнитель':<14} {'Описание':<26} {'Статус':<22}")
    sep = "=" * len(header)
    print(sep)
    print(header)
    print(sep)

    for task in task_list:
        print(f"{task.date_issued.format():<22} "
              f"{task.deadline.format():<22} "
              f"{task.executor:<14} "
              f"{task.description:<26} "
              f"{task.status:<22}")
    print(sep)


def get_current_datetime() -> DateTime:
    """
    Возвращает текущую дату и время, не используя библиотеки.
    Запрашивает дату у пользователя.
    """
    while True:
        print("\nДля работы отчётов необходимо знать сегодняшнюю дату.")
        print("Введите дату в формате ГГГГ ММ ДД ЧЧ ММ")
        print("(например: 2026 5 10 12 30)")
        user_input = input("> ").strip()
        parts = user_input.split()
        if len(parts) == 5:
            try:
                y, m, d, h, minu = [int(p) for p in parts]
                return DateTime(y, m, d, h, minu)
            except Exception:
                pass
        print("Неверный формат. Попробуйте ещё раз.")


def main():
    """
    Главная функция. Загрузка данных, меню, вызов отчётов.
    """
    print("=" * 50)
    print("     СЕМЕЙНЫЙ МЕНЕДЖЕР ЗАДАЧ")
    print("=" * 50)

    tasks = load_from_file("family_tasks.txt")
    if not tasks:
        print("Создаётся демонстрационная база из 30 задач.")
        tasks = create_base()
        save_to_file("family_tasks.txt", tasks)

    now = get_current_datetime()
    print(f"\nТекущая дата установлена: {now.format()}")

    while True:
        print("\n╔════════════════════════════════╗")
        print("║     СЕМЕЙНЫЙ МЕНЕДЖЕР ЗАДАЧ    ║")
        print("╠════════════════════════════════╣")
        print("║ 1. Показать все задачи         ║")
        print("║ 2. Отчёт: последние N дней     ║")
        print("║ 3. Отчёт: провалы сотрудника   ║")
        print("║ 4. Отчёт: задачи в исполнении  ║")
        print("║ 0. Выход                       ║")
        print("╚════════════════════════════════╝")

        choice = input("Ваш выбор: ").strip()

        if choice == "0":
            print("Завершение работы. До свидания!")
            break
        elif choice == "1":
            print("\n--- Полный список задач ---")
            print_tasks(tasks)
        elif choice == "2":
            while True:
                try:
                    n = int(input("Введите количество прошедших дней (N): "))
                    if n < 0:
                        print("Ошибка: число не может быть отрицательным.")
                        continue
                    break
                except Exception:
                    print("Ошибка: введите целое число.")
            result = report_1_last_n_days(tasks, n, now)
            print(f"\n--- Отчёт 1: Задачи за последние {n} дней ---")
            print_tasks(result)
        elif choice == "3":
            while True:
                member = input("Введите имя члена семьи "
                               "(Папа, Мама, Сын, Дочь): ").strip()

                if not member:
                    print("Ошибка: имя не может быть пустым.")
                    continue

                allowed_names = ["Папа", "Мама", "Сын", "Дочь"]
                if member not in allowed_names:
                    print(f"Ошибка: '{member}' — недопустимое имя.")
                    print("Допустимые имена: Папа, Мама, Сын, Дочь.")
                    continue

                break

            result = report_2_failed_by_member(tasks, member)
            print(f"\n--- Отчёт 2: Проваленные задачи — {member} ---")
            print_tasks(result)
        elif choice == "4":
            result = report_3_in_progress(tasks)
            print("\n--- Отчёт 3: Задачи в исполнении "
                  "(получена / в процессе) ---")
            print_tasks(result)
        else:
            print("Ошибка: такого пункта нет. Выберите 0–4.")


if __name__ == "__main__":
    main()