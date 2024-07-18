import logging

from core.app import App

# Create a console handler and set its level to INFO
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handler
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)


# Add the handler to the logger
logger = logging.getLogger()
logger.addHandler(ch)

if __name__ == '__main__':
    App("Lionel Messi")
