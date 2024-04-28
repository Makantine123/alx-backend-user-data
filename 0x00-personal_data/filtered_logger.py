#!/usr/bin/env python3
"""Module for personal data"""

from typing import List
from os import environ
import re
import logging
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """"Function"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}',
                         message)

    return message


def get_logger() -> logging.Logger:
    """Returns a Logger Object named user_data"""
    logger = logging.getLogger("userdata")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db():
    """functioon"""
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = environ.get("PERSONAL_DATA_DB_NAME")

    connect = mysql.connector.connection.MySQLConnection(user=username,
                                                         password=password,
                                                         host=host,
                                                         database=dbname)
    return connect


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION: str = "***"
    FORMAT: str = "[HOLBERTON] %(name)s \
%(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR: str = ";"

    def __init__(self, fields: List[str]):
        """Initialisation Method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fileds = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(self.fileds, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
