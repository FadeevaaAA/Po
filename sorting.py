def shell_sort(tasks: list, key_funcs: list):
    """
    Сортировка списка задач методом Шелла с поддержкой цепочки ключей.

    Параметры:
        tasks: список объектов Task.
        key_funcs: список функций, каждая принимает Task и возвращает число/строку.
                   Сравнение идёт последовательно по ключам.
    """
    n = len(tasks)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = tasks[i]
            j = i
            while j >= gap:
                should_shift = False
                for key_func in key_funcs:
                    left_val = key_func(tasks[j - gap])
                    right_val = key_func(temp)
                    if left_val < right_val:
                        # Правильный порядок, не сдвигаем
                        break
                    elif left_val > right_val:
                        # Порядок нарушен, сдвигаем
                        should_shift = True
                        break
                    # Если равны — проверяем следующий ключ
                if should_shift:
                    tasks[j] = tasks[j - gap]
                    j -= gap
                else:
                    break
            tasks[j] = temp
        gap //= 2