import logging
import os

def setup_logger():
    """
    Настраивает логгер для записи ошибок в файл errors.log
    """
    logger = logging.getLogger("low_level_errors")
    logger.setLevel(logging.ERROR)

    log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "errors.log"))
    file_handler = logging.FileHandler(log_file)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger