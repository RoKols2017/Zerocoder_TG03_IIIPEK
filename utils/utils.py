import logging

def set_loglevel(level: str):
    match level.upper():
        case 'DEBUG':
            logging.basicConfig(level=logging.DEBUG)
        case 'INFO':
            logging.basicConfig(level=logging.INFO)
        case 'WARNING':
            logging.basicConfig(level=logging.WARNING)
        case 'ERROR':
            logging.basicConfig(level=logging.ERROR)
        case 'CRITICAL':
            logging.basicConfig(level=logging.CRITICAL)
