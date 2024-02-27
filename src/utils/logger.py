import sys
import logging
from datetime import datetime

class handle_error:
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __call__(self, func):
        def func_decorated(instance, *args, **kwargs):
            logger: logging.Logger = getattr(instance, 'logger')
            try:
                return func(instance, *args, **kwargs)
            except Exception as e:
                logger.error(self.error_message + ' : ' + str(e))
                sys.exit(1)
        return func_decorated

def get_logger(user_name: str) -> logging.Logger:
    logger = logging.getLogger()

    # generate log file name
    timestamp = datetime.strftime(datetime.now(), r'%Y%M%d_%H%M%S')
    log_file = timestamp + '_' + user_name + '.log'

    # configure log formatter
    formatter = logging.Formatter(
        '%(asctime)s, ' + user_name + ' - %(levelname)s - %(message)s',
        r'%Y-%m-%d %H:%M:%S'
    )

    # configure handlers
    handlers: list[logging.Handler] = [
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout),
    ]

    # register handlers
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    return logger
