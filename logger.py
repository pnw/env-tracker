import logging

logging.basicConfig()
log = logging.getLogger('et')
log.setLevel(logging.DEBUG)
print(log.level)