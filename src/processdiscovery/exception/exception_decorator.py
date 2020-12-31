from functools import wraps


class InvalidRaiseException(Exception):
    pass

# class TimeoutException(Exception):
#     def __init__(self, msg=None):
#         #: The message from the remark tag or element
#         self.msg = msg
#
#     def __str__(self):
#         if self.msg is None:
#             return "No error message provided"
#         if not isinstance(self.msg, str):
#             return str(self.msg)
#         return self.msg


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
