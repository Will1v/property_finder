import logging

logger_instances = {}

def get_logger(logger_name, debug: bool = False):
    logger = logger_instances.get(logger_name, logging.getLogger(logger_name))
    logger_level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(logger_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger_level)  # Set to INFO level
    formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)d][%(levelname)s] %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger_instances[logger_name] = (logger, console_handler)
    return logger

def set_all_loggers_debug(debug: bool):
    print(f"Setting debug = {debug} for all loggers")
    for logger_name in logger_instances:
        logger, console_handler = logger_instances[logger_name]
        log_level = logging.DEBUG if debug else logging.INFO
        logger.setLevel(log_level)
        console_handler.setLevel(log_level)
