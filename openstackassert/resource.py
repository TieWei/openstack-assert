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

        if 'ensure' in kwargs and kwargs['ensure'] in ['all', 'one']:
            ensure = kwargs.pop('ensure')
        else:
            ensure = 'all'

        function._validate = {'present': present, 'ensure': ensure}
        return function

    if kwargs:
        return decorator
    else:
        return decorator(args[0])

def assert_wrapper(func):
    ensure = func._validate['ensure']
    present = func._validate['present']
    @wraps(func)
    def result(*args, **kwargs):
        result = False
        try:
            details = func(*args, **kwargs)
            if isinstance(details, list) and len(details) > 0:
                result = True if ensure == 'all' else False
                for one in details:
                    if isinstance(one, dict) and 'assert' in one:
                        one_result = False if one['assert'] is None else True
                        if ensure == 'all':
                            result = result & one_result
                        else:
                            result = result | one_result

            elif details is not None:
                result = True
        except OpenstackAssertException as e:
            logging.exception(e.message)
            if config.stop:
                raise e
            result = not(present)
        finally:
            result = not(result ^ present)
            return result
    return result


class Resource(object):

    def __init__(self, details=None):
        self._details = details if details else {}
        for attr in dir(self):
            func = getattr(self, attr)
            if hasattr(func, '_detect') and hasattr(func, '_present'):
                raise Exception("resource can be either detectable or validatable")
            if hasattr(func, '_detect'):
                setattr(self, "_%s" % func._detect, func())
            elif hasattr(func, "_validate"):
                if func._validate['present']:
                    assure_name = "has_%s" % func.__name__
                else:
                    assure_name = "not_has_%s" % func.__name__
                setattr(self, assure_name, assert_wrapper(func))

    def _fetch_and_return(fetch_func, key):
        if key not in self._details:
            fetch_func(self)
        return self._details.get(key, None)



