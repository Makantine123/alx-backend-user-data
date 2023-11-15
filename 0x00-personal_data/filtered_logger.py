#!/usr/bin/env python3
"""Module for personal data"""


import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, seperator: str
        ) -> str:
    """filter_datum function"""
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, seperator), replace(redaction), message)
