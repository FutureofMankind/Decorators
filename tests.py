import os
import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        call_time = datetime.datetime.now()
        time_format = call_time.strftime('%d/%m/%Y, %H:%M:%S')
        name_func = old_function.__name__
        arguments = f'{args}, {kwargs}'
        result = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as log_file:
            write = f'Дата и время вызова функции: {time_format}\n ' \
                    f'Функция: {name_func}\n Аргументы: {arguments}\n Возвращаемое значение: {result}\n\n'
            log_file.writelines(write)
        return result
    return new_function

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            call_time = datetime.datetime.now()
            time_format = call_time.strftime('%d/%m/%Y, %H:%M:%S')
            name_func = old_function.__name__
            arguments = f'{args}, {kwargs}'
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as log_file:
                write = f'Дата и время вызова функции: {time_format}\n ' \
                        f'Функция: {name_func}\n Аргументы: {arguments}\n Возвращаемое значение: {result}\n\n'
                log_file.writelines(write)
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


@logger('main3.log')
def flat_generator(list_of_list):
    for listing in list_of_list:
        if type(listing) is list:
            yield from flat_generator(listing)
        else:
            yield listing

def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    print(list(flat_generator(list_of_lists_2)))