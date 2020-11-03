import datetime
import logging
import baostock as bs


class BsUtils():

    def __init__(self):
        pass

    @staticmethod
    def login():
        lg = bs.login()
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)


    def getAllStock(self):
        rs = bs.query_all_stock()
        print('query_all_stock respond error_code:' + rs.error_code)
        print('query_all_stock respond  error_msg:' + rs.error_msg)
        data_list = []
        while (rs.error_code == '0') and rs.next():
            data_list.append(rs.get_row_data())
        return data_list