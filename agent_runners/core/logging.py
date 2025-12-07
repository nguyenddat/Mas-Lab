import logging

def setup_agent_runners_logger():
    """
    Sets up the logger for the 'agent_runners' module.
    """
    logger = logging.getLogger('agent_runners')
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

logger = setup_agent_runners_logger()