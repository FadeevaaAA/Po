from sorting import shell_sort


def report_1_last_n_days(tasks: list, n: int, now) -> list:
    # Фильтрация: разница в днях между now и датой выдачи <= n
    filtered = []
    for t in tasks:
        diff = t.date_issued.days_until(now)  # now - issued
        if 0 <= diff <= n:
            filtered.append(t)

    def status_order(task):
        order = {
            "в процессе": 0,
            "получена": 1,
            "провалена": 2,
            "успешно выполнена": 3
        }
        return order.get(task.status, 99)

    shell_sort(filtered, [
        lambda t: -t.date_issued.to_minutes(),  # по убыванию даты выдачи
        status_order                             # по приоритету статуса
    ])
    return filtered


def report_2_failed_by_member(tasks: list, member: str) -> list:
    filtered = [t for t in tasks
                if t.executor == member and t.status == "провалена"]

    shell_sort(filtered, [
        lambda t: -t.deadline.to_minutes(),  # по убыванию дедлайна
        lambda t: t.description               # по возрастанию описания
    ])
    return filtered


def report_3_in_progress(tasks: list) -> list:
    filtered = [t for t in tasks
                if t.status in ("получена", "в процессе")]

    shell_sort(filtered, [
        lambda t: t.executor,                # по возрастанию имени
        lambda t: t.deadline.to_minutes()    # по возрастанию дедлайна
    ])
    return filtered