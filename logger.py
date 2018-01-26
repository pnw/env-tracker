import logging as _logging

_logging.basicConfig(format='%(levelname)-7s [%(module)s:%(filename)s:%(lineno)s] %(message)s')
logger = _logging.getLogger('et')
logger.setLevel(_logging.ERROR)
