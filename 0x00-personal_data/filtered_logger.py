#!/usr/bin/env python3
"""Module for personal data"""


import re


def filter_datum(fields, redaction, message, separator):
    """Function"""
    return re.sub(
        r'(?:(?<=^)|(?<=\{})){}=[^{}]*'.
        format(separator, '|'.
               join(fields), separator), '{}={}'.
        format(redaction, redaction), message)
