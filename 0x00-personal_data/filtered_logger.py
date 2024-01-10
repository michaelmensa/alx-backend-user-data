#!/usr/bin/env python3
'''
Module filtered_logger.py
'''
import logging
import re
import os
from typing import List
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' function that returns the log message obfuscated
    args:
        fields: list of strings representing all fields to obfuscate
        redaction: string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a str rep by which char is separating all fields in the
                    log line
    '''
    pattern = r'(' + '|'.join(map(re.escape, fields)) +\
              r')=(.*?)(?=' + re.escape(separator) + '|$)'
    return re.sub(pattern, rf'\1={redaction}', message)


def get_logger() -> logging.Logger:
    ''' function that takes no args and returns logging.Logger object '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' function that returns a connector to the database '''
    db_config = {
            'user': os.getenv('PERSONAL_DATA_DB_USERNAME'),
            'db': os.getenv('PERSONAL_DATA_DB_NAME'),
            'passwd': os.getenv('PERSONAL_DATA_DB_PASSWORD'),
            'host': os.getenv('PERSONAL_DATA_DB_HOST')
            }

    cnx = mysql.connector.connect(**db_config)

    return cnx


def main():
    ''' main function '''
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    fields = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        ''' constructor method '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' method to filter values in incoming log records
        using filter_datum.
        '''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == '__main__':
    main()
