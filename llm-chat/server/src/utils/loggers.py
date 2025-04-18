import logging

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the given name and level

    Args:
        name (str): The name of the logger
        level (int): The logging level (default is logging.INFO)

    Returns:
        logging.Logger: The configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
