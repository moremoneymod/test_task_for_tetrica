# Функция, отсекающая лишние интервалы и корректирующая подходящие (устанавливает границы интервала в рамках урока)
def clean_intervals(raw_intervals: list[list[int]], lesson: list[int]) -> list[list[int]]:
    correct_intervals = []
    for index in range(len(raw_intervals)):
        current_interval = raw_intervals[index]
        if current_interval[0] < lesson[0] or current_interval[1] > lesson[1] or current_interval[0] > lesson[1]:
            if (current_interval[0] < lesson[0] and current_interval[1] < lesson[0]) or (
                    current_interval[0] > lesson[1] and current_interval[1] > lesson[1]):
                continue
            if current_interval[0] < lesson[0]:
                current_interval[0] = lesson[0]
                correct_intervals.append(current_interval)
            if current_interval[1] > lesson[1]:
                current_interval[1] = lesson[1]
                correct_intervals.append(current_interval)
        else:
            correct_intervals.append(current_interval)
    return correct_intervals


# Функция для объединения интервалов
def union_intervals(raw_intervals: list[list[int]]) -> list[list[int]]:
    temp_interval = raw_intervals[0]
    correct_intervals = []
    for ij in range(1, len(raw_intervals)):
        current_interval = raw_intervals[ij]

        if current_interval[0] <= temp_interval[1]:
            if current_interval[1] <= temp_interval[1]:
                continue
            elif current_interval[1] > temp_interval[1]:
                temp_interval[1] = current_interval[1]
        else:
            correct_intervals.append(temp_interval)
            temp_interval = current_interval
    correct_intervals.append(temp_interval)
    return correct_intervals


def appearance(intervals: dict[str, list[int]]) -> int:
    pupil_raw_intervals = intervals["pupil"]
    tutor_raw_intervals = intervals["tutor"]
    lesson = intervals["lesson"]
    pupil_intervals = [[pupil_raw_intervals[index], pupil_raw_intervals[index + 1]] for index in
                       range(0, len(pupil_raw_intervals), 2)]
    tutor_intervals = [[tutor_raw_intervals[index], tutor_raw_intervals[index + 1]] for index in
                       range(0, len(tutor_raw_intervals), 2)]

    total = 0

    if len(pupil_intervals) == 0 or len(tutor_intervals) == 0 or len(lesson) == 0:
        return 0

    pupil_intervals = clean_intervals(pupil_intervals, lesson)
    tutor_intervals = clean_intervals(tutor_intervals, lesson)

    if len(pupil_intervals) != 0 or len(tutor_intervals) != 0:
        pupil_intervals = union_intervals(pupil_intervals)
        tutor_intervals = union_intervals(tutor_intervals)

    for tutor_interval_index in range(len(tutor_intervals)):
        current_tutor_interval = tutor_intervals[tutor_interval_index]
        for pupil_interval_index in range(0, len(pupil_intervals)):
            current_pupil_interval = pupil_intervals[pupil_interval_index]

            if current_pupil_interval[0] >= current_tutor_interval[0] and current_pupil_interval[0] < \
                    current_tutor_interval[1]:
                if current_pupil_interval[1] <= current_tutor_interval[1]:
                    total += current_pupil_interval[1] - current_pupil_interval[0]
                elif current_pupil_interval[1] > current_tutor_interval[1]:
                    total += current_tutor_interval[1] - current_pupil_interval[0]
                    current_pupil_interval[0] = current_tutor_interval[1]

            elif current_pupil_interval[0] < current_tutor_interval[0] and current_pupil_interval[1] > \
                    current_tutor_interval[0]:
                if current_pupil_interval[1] <= current_tutor_interval[1]:
                    total += current_pupil_interval[1] - current_tutor_interval[0]
                elif current_pupil_interval[1] > current_tutor_interval[1]:
                    total += current_tutor_interval[1] - current_tutor_interval[0]

    return total


tests = [
    # Полное пересечение всех интервалов
    {'intervals': {'lesson': [100, 200],
                   'pupil': [100, 200],
                   'tutor': [100, 200]},
     'answer': 100
     },
    # Урок идет, но ни ученик, ни учитель не присутствуют
    {'intervals': {'lesson': [100, 200],
                   'pupil': [],
                   'tutor': []},
     'answer': 0
     },
    # Ученик и учитель присутствуют до начала урока
    {'intervals': {'lesson': [100, 200],
                   'pupil': [50, 90],
                   'tutor': [60, 95]},
     'answer': 0
     },
    # Ученик и учитель присутствуют после урока
    {'intervals': {'lesson': [100, 200],
                   'pupil': [210, 300],
                   'tutor': [220, 310]},
     'answer': 0
     },
    # Присутствие перекрывает начало урока
    {'intervals': {'lesson': [100, 200],
                   'pupil': [50, 150],
                   'tutor': [120, 180]},
     'answer': 30
     },
    # Присутствие перекрывает конец урока
    {'intervals': {'lesson': [100, 200],
                   'pupil': [150, 250],
                   'tutor': [180, 300]},
     'answer': 20
     },
    # Ученик и учитель пересекаются частично внутри урока
    {'intervals': {'lesson': [100, 200],
                   'pupil': [110, 150, 160, 180],
                   'tutor': [120, 140, 170, 190]},
     'answer': 30
     },
    # Несколько интервалов, ученик и учитель не совпадают
    {'intervals': {'lesson': [100, 300],
                   'pupil': [110, 120, 150, 160],
                   'tutor': [130, 140, 170, 180]},
     'answer': 0
     },
    # Ученик и учитель присутствуют полностью в уроке, но с разрывами
    {'intervals': {'lesson': [100, 500],
                   'pupil': [120, 200, 300, 400],
                   'tutor': [150, 250, 350, 450]},
     'answer': 100
     },
    # Ученик и учитель полностью покрывают урок
    {'intervals': {'lesson': [100, 500],
                   'pupil': [50, 550],
                   'tutor': [70, 530]},
     'answer': 400
     },
    # Только одна точка пересечения
    {'intervals': {'lesson': [100, 200],
                   'pupil': [150, 160],
                   'tutor': [160, 170]},
     'answer': 0
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test[
            'answer'], f'Error on additional test case {i}, got {test_answer}, expected {test["answer"]}'
    print("All tests passed!")
