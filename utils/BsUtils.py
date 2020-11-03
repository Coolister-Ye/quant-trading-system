import datetime
import logging
import baostock as bs


class BsUtils():

    def __init__(self):
        pass

    @staticmethod
    def login():
        lg = bs.login()
        logging.info('login respond error_code:' + lg.error_code)
        logging.info('login respond  error_msg:' + lg.error_msg)


