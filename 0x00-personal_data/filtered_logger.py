#!/usr/bin/env python3
"""Module for personal data"""


import re


def filter_datum(fields, redaction, message, seperator):
    """filter_datum function"""
    for field in fields:
        message = re.sub(f'{field}=.*?{seperator}',
                         f'{field}={redaction}{seperator}', message)
    return message
