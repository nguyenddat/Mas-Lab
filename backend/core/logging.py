import logging

def setup_logger():
    """
    Sets up the logger for the 'backend' module.
    """
    logger = logging.getLogger('backend')
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if called multiple times
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

logger = setup_logger()