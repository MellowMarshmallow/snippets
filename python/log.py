#!/usr/bin/env python


import logging


def get_pretty_handler(level):
    try:
        from colorlog import ColoredFormatter
    except ModuleNotFoundError:
        formatter = logging.Formatter("%(levelname)-8s | %(message)s")
    else:
        formatter = ColoredFormatter("%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s")

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    return handler


def create_logger(level, *handlers, name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    for handler in handlers:
        logger.addHandler(handler)


def test_logs(logger):
    logger.debug("For developers")
    logger.info("For the curious")
    logger.warning("Oh no")
    logger.error("Serious stuff")
    logger.critical("Everything is on fire")


if __name__ == "__main__":
    handler = get_pretty_handler(logging.DEBUG)
    create_logger(logging.DEBUG, handler)
    test_logs(logging.getLogger(__name__))
