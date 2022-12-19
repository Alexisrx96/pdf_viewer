from logging import (INFO, FileHandler, Formatter, Handler, Logger,
                     StreamHandler, getLogger)

from envs import EnvVars

FORMAT = Formatter('%(asctime)s %(message)s')


def set_handler(handler: Handler, logger: Logger):
    handler.setFormatter(FORMAT)
    handler.setLevel(INFO)
    logger.addHandler(handler)


def get_logger(name: str) -> Logger:
    logger = getLogger(name)
    if EnvVars.log_to_console:
        set_handler(StreamHandler(), logger)
    if EnvVars.log_to_file:
        set_handler(FileHandler(EnvVars.log_file), logger)
    return logger


logger = get_logger('pdf_viewer')
