#!/usr/bin/env python3
"""Module for personal data"""


import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """filter_datum function"""
    for field in fields:
        message = re.sub(f'{field}=.*?{seperator}',
                         f'{field}={redaction}{seperator}', message)
    return message
