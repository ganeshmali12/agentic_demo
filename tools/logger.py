import logging
import colorlog


def setup_logger():
    logger = colorlog.getLogger("AutonomousAgent")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = colorlog.StreamHandler()

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s | %(message)s",
        log_colors={
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
        },
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logger()