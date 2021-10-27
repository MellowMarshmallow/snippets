#!/usr/bin/env python


import logging
import json
from random import randint
import time
from threading import Semaphore
from colorlog import ColoredFormatter
from flask import Flask


app = Flask(__name__)
sem = Semaphore()


@app.before_first_request
def init():
    # remove existing handlers
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    # configure logging system
    log_level = logging.DEBUG

    formatter = ColoredFormatter(
        " | ".join(
            [
                f"%(log_color)s{prop}%(reset)s"
                for prop in [
                    "%(levelname)-8s",
                    "%(module)-10s",
                    "%(funcName)-20s",
                    "%(lineno)-4d",
                    "%(message)s",
                ]
            ]
        )
    )

    # genearte a handler and add it to logger
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    app.logger.setLevel(log_level)
    app.logger.addHandler(handler)


@app.after_request
def after_request_func(response):
    # start timer
    tic = time.perf_counter()

    # read response
    res = response.get_json()

    # do logging
    try:
        # only let one thread access the stream handler at a time
        sem.acquire()
        logs = res["logs"]
    except KeyError:
        app.logger.warning("Unable to acquire logs")
    else:
        for log in logs:
            app.logger.log(log["level"], log["message"])
    finally:
        sem.release()

    # only return the return object
    response.data = json.dumps(res.get("return_obj"))

    # end timer
    toc = time.perf_counter()
    app.logger.debug(f"Took {toc - tic:0.4f} seconds")

    return response


@app.route("/")
def index():
    logs = []

    time.sleep(seconds := randint(0, 5))
    logs.append({"message": f"First message took {seconds}", "level": logging.WARNING})

    time.sleep(seconds := randint(0, 5))
    logs.append({"message": f"Second message took {seconds}", "level": logging.ERROR})

    time.sleep(seconds := randint(0, 5))
    logs.append({"message": f"Third message took {seconds}", "level": logging.CRITICAL})

    return {"logs": logs, "return_obj": "Hello, World"}
