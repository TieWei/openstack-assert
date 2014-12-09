import logging
import config
from functools import wraps

def detectable(*args, **kwargs):

    def decorator(function):
        if 'name' in kwargs:
            name = kwargs.pop('name')
        else:
            name = function.__name__
        function._detect = name
        return function

    if kwargs:
        return decorator
    else:
        return decorator(args[0])

def validatable(*args, **kwargs):

    def decorator(function):
        if 'present' in kwargs:
            present = kwargs.pop('present')
            if not isinstance(present, bool):
                raise Exception("validatable's present should be bool type")
        else:
            present = True

        function._present = present
        return function

    if kwargs:
        return decorator
    else:
        return decorator(args[0])

def assert_wrapper(func):
    present = func._present
    @wraps(func)
    def result(*args, **kwargs):
        result = False
        try:
            details = func(*args, **kwargs)
            if details is not None:
                result = True
        except OpenstackAssertException as e:
            logging.exception(e.message)
            if config.stop:
                raise e
            result = not(present)
        finally:
            return not(result^present)
    return result


class Resource(object):

    def __init__(self):
        for attr in dir(self):
            func = getattr(self, attr)
            if hasattr(func, '_detect') and hasattr(func, '_present'):
                raise Exception("resource can be either detectable or validatable")
            if hasattr(func, '_detect'):
                setattr(self, "_%s" % func._detect, func())
            elif hasattr(func, "_present"):
                if func._present:
                    assure_name = "has_%s" % func.__name__
                else:
                    assure_name = "not_has_%s" % func.__name__
                setattr(self, assure_name, assert_wrapper(func))



