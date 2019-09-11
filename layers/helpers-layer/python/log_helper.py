import traceback
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg , "headers": {}, "statusCode": 400,
        "isBase64Encoded":"false"}