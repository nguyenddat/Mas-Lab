import logging

def setup_mcp_logger():
    """
    Sets up the logger for the 'mcp' module.
    """
    logger = logging.getLogger('mcp')
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

logger = setup_mcp_logger()