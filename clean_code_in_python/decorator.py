import functools
import time
from datetime import datetime


def hide_field(field) -> str:
    return "**민감한 정보 삭제**"


def format_time(field_timestamp: datetime) -> str:
    return field_timestamp.strptime('%Y-%M-%')


def traced_function_wrong(function):
    print(f'{function} 함수 실행')
    start_time = time.time()

    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        result = function(*args, **kwargs)
        print(f'함수 {function}의 실행시간: {time.time() - start_time}')
        return result

    return wrapped


@traced_function_wrong
def process_with_delay(callback, delay=0):
    time.sleep(delay)
    return callback()
