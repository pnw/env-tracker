import logging as _logging

_logging.basicConfig(format='%(levelname)-7s [%(module)s:%(filename)s:%(lineno)s] %(message)s')
log = _logging.getLogger('et')
log.setLevel(_logging.DEBUG)
