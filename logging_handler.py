import logging
from config import LOG_PATH
from os import makedirs


def setup_logging():
    makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        encoding='utf-8',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logging.getLogger().addHandler(console_handler)


# Initialize logger
setup_logging()
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    pass
