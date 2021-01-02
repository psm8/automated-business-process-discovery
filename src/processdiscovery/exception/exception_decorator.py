from functools import wraps
from threading import Thread


class InvalidRaiseException(Exception):
    pass


def only_throws(E):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except E:
                raise
            except InvalidRaiseException:
                raise
            except Exception as e:
                raise InvalidRaiseException("got %s, expected %s, from %s" % (
                    e.__class__.__name__, E.__name__, f.__name__)
                )

        return wrapped
    return decorator


class TimeoutException(Exception):
    def __init__(self, msg=None):
        #: The message from the remark tag or element
        self.msg = msg

    def __str__(self):
        if self.msg is None:
            return "No error message provided"
        if not isinstance(self.msg, str):
            return str(self.msg)
        return self.msg


def timeout(seconds_before_timeout):
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = [TimeoutException('timeout [%s seconds] exceeded!' % seconds_before_timeout)]

            def new_func():
                try:
                    res[0] = func(*args, **kwargs)
                except BaseException as e:
                    res[0] = e
            t = Thread(target=new_func)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except BaseException as e:
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco



