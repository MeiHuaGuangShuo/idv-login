import sys
from loguru import logger as _logger


logger = _logger
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add('log.txt', encoding='utf-8', level="DEBUG")
