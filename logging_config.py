import logging
import os

def setup_logger():
    logger = logging.getLogger("BinanceFuturesBot")
    logger.setLevel(logging.DEBUG)

    # File handler for detailed API logs
    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trading_bot.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger