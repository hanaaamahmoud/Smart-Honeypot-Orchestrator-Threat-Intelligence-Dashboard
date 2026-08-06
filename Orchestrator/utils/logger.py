import logging
import os

##########################################
def setup_logger(logger_name):

    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(f"logs/{logger_name}.log")

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger