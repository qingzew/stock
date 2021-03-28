import logging

# create logger
#logger = logging.getLogger('stock')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create file handler
fh1 = logging.FileHandler('./logs/log')
fh1.setLevel(logging.DEBUG)

fh2 = logging.StreamHandler()
fh2.setLevel(logging.DEBUG)

# create formatter
#fmt = "%(asctime)-15s %(levelname)s %(filename)s line: %(lineno)d pid: %(process)d: %(message)s"
fmt = "%(asctime)-15s %(levelname)s %(filename)s line %(lineno)d: %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

fh1.setFormatter(formatter)
logger.addHandler(fh1)

fh2.setFormatter(formatter)
logger.addHandler(fh2)

