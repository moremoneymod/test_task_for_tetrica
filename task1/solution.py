def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        param_types = {key: annotations[key] for key in annotations if key != "return"}

        param_names = list(param_types.keys())

        if len(args) + len(kwargs) < len(param_types):
            missing_params = [param_name for param_name in param_names if
                              param_name not in kwargs and param_names.index(param_name) >= len(args)]
            raise TypeError(f"Отсутствуют значения для параметров: {' '.join(missing_params)}")

        elif len(args) + len(kwargs) > len(param_types):
            excess_params = (list(args) + list(kwargs.values()))[len(param_types):]
            raise TypeError(f"Переданы лишние значения: {excess_params}")

        for arg, (param_name, expected_type) in zip(args, param_types.items()):
            if not isinstance(arg, expected_type):
                raise TypeError(
                    f"Аргумент {param_name} должен быть типа {expected_type.__name__}, "
                    f"но получен тип {type(arg).__name__}")

        for param_name, arg_value in kwargs.items():
            if param_name not in param_types:
                raise TypeError(f"Неизвестный аргумент {param_name}")
            expected_type = param_types[param_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Аргумент {param_name} должен быть типа {expected_type.__name__}, "
                    f"но получен тип {type(arg_value).__name__}")

        return func(*args, **kwargs)

    return wrapper


# Тестовые функции
@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def concat_strings(a: str, b: str) -> str:
    return a + b


@strict
def multiply(a: int, b: float) -> float:
    return a * b


@strict
def bool_logic(a: bool, b: bool) -> bool:
    return a and b


@strict
def identity(value: str) -> str:
    return value


if __name__ == "__main__":
    # 1. Корректные вызовы функций
    try:
        print(sum_two(1, 2))  # >>> 3
        print("Test 1 passed")
    except TypeError as e:
        print(f"Test 1 failed: {e}")

    try:
        print(concat_strings("hello", "world"))  # >>> helloworld
        print("Test 2 passed")
    except TypeError as e:
        print(f"Test 2 failed: {e}")

    try:
        print(multiply(3, 4.5))  # >>> 13.5
        print("Test 3 passed")
    except TypeError as e:
        print(f"Test 3 failed: {e}")

    try:
        print(bool_logic(True, False))  # >>> False
        print("Test 4 passed")
    except TypeError as e:
        print(f"Test 4 failed: {e}")

    try:
        print(identity("test"))  # >>> test
        print("Test 5 passed")
    except TypeError as e:
        print(f"Test 5 failed: {e}")

    # 2. Некорректные вызовы функций
    try:
        print(sum_two(1, "2"))  # >>> TypeError
        print("Test 6 failed")
    except TypeError as e:
        print(f"Test 6 passed: {e}")

    try:
        print(concat_strings("hello", 2))  # >>> TypeError
        print("Test 7 failed")
    except TypeError as e:
        print(f"Test 7 passed: {e}")

    try:
        print(multiply(3, "4.5"))  # >>> TypeError
        print("Test 8 failed")
    except TypeError as e:
        print(f"Test 8 passed: {e}")

    try:
        print(bool_logic(True, "False"))  # >>> TypeError
        print("Test 9 failed")
    except TypeError as e:
        print(f"Test 9 passed: {e}")

    try:
        print(identity(123))  # >>> TypeError
        print("Test 10 failed")
    except TypeError as e:
        print(f"Test 10 passed: {e}")

    # 3. Лишние или недостающие аргументы
    try:
        print(sum_two(1))  # >>> TypeError
        print("Test 11 failed")
    except TypeError as e:
        print(f"Test 11 passed: {e}")

    try:
        print(sum_two(1, 2, 3))  # >>> TypeError
        print("Test 12 failed")
    except TypeError as e:
        print(f"Test 12 passed: {e}")

    try:
        print(concat_strings("hello"))  # >>> TypeError
        print("Test 13 failed")
    except TypeError as e:
        print(f"Test 13 passed: {e}")

    try:
        print(bool_logic(True, True, False))  # >>> TypeError
        print("Test 14 failed")
    except TypeError as e:
        print(f"Test 14 passed: {e}")

    try:
        print(sum_two(1, 2, 3, 4, a=5, b=6))  # >>> TypeError
        print("Test 15 failed")
    except TypeError as e:
        print(f"Test 15 passed: {e}")
