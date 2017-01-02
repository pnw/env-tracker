import logging

logging.basicConfig(format='%(levelname)-7s [%(module)s:%(filename)s:%(lineno)s] %(message)s')
log = logging.getLogger('et')
log.setLevel(logging.DEBUG)
