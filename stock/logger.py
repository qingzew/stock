import re
import logging
from logging.handlers import TimedRotatingFileHandler


## create logger
#logger = logging.getLogger()
##logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)
#
## create file handler
#fh1 = logging.FileHandler('./logs/log')
##fh1.setLevel(logging.DEBUG)
#fh1.setLevel(logging.ERROR)
#
#
#fh2 = logging.StreamHandler()
##fh2.setLevel(logging.DEBUG)
#fh2.setLevel(logging.ERROR)
#
## create formatter
##fmt = "%(asctime)-15s %(levelname)s %(filename)s line: %(lineno)d pid: %(process)d: %(message)s"
#fmt = "%(asctime)-15s %(levelname)s %(filename)s line %(lineno)d: %(message)s"
#datefmt = "%a %d %b %Y %H:%M:%S"
#formatter = logging.Formatter(fmt, datefmt)
#
#fh1.setFormatter(formatter)
#logger.addHandler(fh1)
#
#fh2.setFormatter(formatter)
#logger.addHandler(fh2)

# create logger
logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

logging.getLogger('dtshare').setLevel(logging.WARNING)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('pyexecjs').setLevel(logging.WARNING)
logging.getLogger('charset_normalizer').setLevel(logging.WARNING)

fmt = '[%(asctime)s] [%(process)d] [%(levelname)s] - %(module)s.%(funcName)s (%(filename)s:%(lineno)d) - %(message)s'
datefmt = "%a %d %b %Y %H:%M:%S"

file_handler = TimedRotatingFileHandler(filename='logs/stock.log', when='MIDNIGHT', interval=1, backupCount=30)
file_handler.suffix = '%Y-%m-%d'
file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")

file_handler.setFormatter(logging.Formatter(fmt, datefmt))
logger.addHandler(file_handler)


term_handler = logging.StreamHandler()
term_handler.setFormatter(logging.Formatter(fmt, datefmt))
logger.addHandler(term_handler)

