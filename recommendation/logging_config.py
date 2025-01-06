import logging

def setup_logger():
    """
    Настраивает корневой логгер для записи логов в файл error.log
    """
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("../errors.log")
        ]
    )
