#!/usr/bin/env python3
"""Module for personal data"""


import re


def filter_datum(fields, redaction, message, separator):
    """"Function"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}',
                         message)

    return message
