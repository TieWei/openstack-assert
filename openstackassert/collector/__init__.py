import config
import sys
import logging

def _load_collector(driver, *args, **kwargs):
    if not driver:
        logging.error("Collector driver option required, but not specified")
        sys.exit(1)
    try:
        module, _, class_name = driver.rpartition('.')
        module = __import__(module)
        return getattr(module, class_name)
    except (ValueError, AttributeError):
        raise ImportError('Collector <%s> cannot be found' % class_name)


driver = _load_collector(config.collector)()