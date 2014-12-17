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
                ensure_all = lambda pre,one: pre & (one['present'] == True)
                ensure_one = lambda pre,one: pre | (one['present'] == True)
                if ensure == 'all':
                    result = reduce(ensure_all, details, 
                                    initializer={'present':True})
                else:
                    result = reduce(ensure_one, details,
                                    initializer={'present':False})
            else:
                result = details['present']
        except OpenstackAssertException as e:
            logging.exception(e.message)
            if config.stop:
                raise e
            result = not(present)
        finally:
            result = (result == present)
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

    def _return_or_fetch(self, fetch_func, key, force=False):
        if key not in self._details or force:
            fetch_func()
        return self._details.get(key, None)



