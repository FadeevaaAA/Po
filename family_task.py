class DateTime:
    def __init__(self, year: int, month: int, day: int,
                 hour: int = 0, minute: int = 0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def to_minutes(self) -> int:
        total_days = self.year * 365 + self.month * 30 + self.day
        total_minutes = total_days * 24 * 60 + self.hour * 60 + self.minute
        return total_minutes

    def days_until(self, other: 'DateTime') -> int:
        return (other.to_minutes() - self.to_minutes()) // (24 * 60)

    def format(self) -> str:
        return (f"{self.day:02d}.{self.month:02d}.{self.year} "
                f"{self.hour:02d}:{self.minute:02d}")

    def to_iso(self) -> str:
        return (f"{self.year:04d}-{self.month:02d}-{self.day:02d}T"
                f"{self.hour:02d}:{self.minute:02d}")

    @staticmethod
    def from_iso(iso_str: str) -> 'DateTime':
        try:
            date_part, time_part = iso_str.split('T')
            year, month, day = date_part.split('-')
            hour, minute = time_part.split(':')
            return DateTime(int(year), int(month), int(day),
                            int(hour), int(minute))
        except Exception:
            raise Exception(f"Неверный формат даты: {iso_str}")


class Task:
    def __init__(self, date_issued: DateTime, deadline: DateTime,
                 executor: str, description: str, status: str):
        self.date_issued = date_issued
        self.deadline = deadline
        self.executor = executor
        self.description = description
        self.status = status

    def __repr__(self):
        return (f"{self.date_issued.to_iso()} | {self.deadline.to_iso()} | "
                f"{self.executor} | {self.description} | {self.status}")


def create_base() -> list:
    tasks = []
    Y, M, D = 2026, 5, 10  # условное сегодня

    def add(issued_offset_days, deadline_offset_days,
            executor, desc, status):
        issued = DateTime(Y, M, D + issued_offset_days, 10, 0)
        deadline = DateTime(Y, M, D + deadline_offset_days, 18, 0)
        tasks.append(Task(issued, deadline, executor, desc, status))

    # Группа 1: выдано 1 день назад
    add(-1, 2, "Папа", "Сходить в магазин", "успешно выполнена")
    add(-1, 1, "Мама", "Помыть окно в комнате", "провалена")
    add(-1, 3, "Папа", "Вынести мусор", "получена")
    add(-1, 0, "Сын", "Сделать уроки", "в процессе")

    # Группа 2: выдано 2 дня назад
    add(-2, 4, "Мама", "Приготовить ужин", "успешно выполнена")
    add(-2, 1, "Сын", "Вынести мусор", "провалена")
    add(-2, 5, "Папа", "Починить кран", "получена")
    add(-2, 2, "Мама", "Погладить бельё", "в процессе")

    # Группа 3: выдано 3 дня назад
    add(-3, 3, "Дочь", "Полить цветы", "провалена")
    add(-3, 1, "Папа", "Пропылесосить", "успешно выполнена")
    add(-3, 7, "Сын", "Погулять с собакой", "получена")
    add(-3, 6, "Мама", "Купить подарок", "в процессе")

    # Группа 4: выдано 4 дня назад
    add(-4, 2, "Дочь", "Сходить в магазин", "провалена")
    add(-4, 3, "Папа", "Заплатить за свет", "получена")
    add(-4, 5, "Сын", "Помыть посуду", "получена")

    # Группа 5: выдано 5 дней назад
    add(-5, 1, "Мама", "Постирать шторы", "успешно выполнена")
    add(-5, 2, "Папа", "Сделать уроки", "в процессе")
    add(-5, 4, "Дочь", "Приготовить ужин", "провалена")
    add(-5, 3, "Сын", "Помыть окно", "провалена")

    # Группа 6: выдано 6 дней назад
    add(-6, 5, "Мама", "Заплатить за газ", "получена")
    add(-6, 6, "Папа", "Отвезти в кружок", "в процессе")
    add(-6, 1, "Дочь", "Вынести мусор", "получена")

    # Группа 7: выдано 7 дней назад
    add(-7, 2, "Сын", "Покормить кота", "успешно выполнена")
    add(-7, 3, "Мама", "Сходить в аптеку", "провалена")
    add(-7, 4, "Папа", "Помыть машину", "в процессе")

    # Группа 8: выдано 8 дней назад
    add(-8, 1, "Дочь", "Прочитать книгу", "получена")
    add(-8, 5, "Сын", "Убрать игрушки", "получена")

    # Группа 9: выдано 9 дней назад
    add(-9, 2, "Мама", "Испечь пирог", "успешно выполнена")
    add(-9, 3, "Папа", "Повесить полку", "в процессе")
    add(-9, 4, "Дочь", "Сделать влажную уборку", "провалена")

    return tasks


def save_to_file(filename: str, tasks: list):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for task in tasks:
                line = (f"{task.date_issued.to_iso()}|{task.deadline.to_iso()}|"
                        f"{task.executor}|{task.description}|{task.status}\n")
                f.write(line)
    except Exception:
        print(f"Ошибка при сохранении файла '{filename}'.")


def load_from_file(filename: str) -> list:
    tasks = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    print(f"Предупреждение: строка {line_num} пропущена "
                          f"(неверное число полей).")
                    continue
                try:
                    issued = DateTime.from_iso(parts[0])
                    deadline = DateTime.from_iso(parts[1])
                except Exception:
                    print(f"Предупреждение: строка {line_num} пропущена "
                          f"(ошибка формата даты/времени).")
                    continue
                tasks.append(Task(issued, deadline,
                                  parts[2], parts[3], parts[4]))
    except Exception:
        print(f"Файл '{filename}' не найден или повреждён. Будет создана новая база.")
    return tasks