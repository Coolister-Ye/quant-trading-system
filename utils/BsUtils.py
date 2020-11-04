import os
import baostock as bs
from pathlib import Path
from utils.FileUtils import FileUtils
from utils.DbUtils import DbUtils
from datetime import date, timedelta

class BsUtils(DbUtils, FileUtils):

    def __init__(self):
        super().__init__()
        self.isSaveToLocal = True
        self.isSaveToMysql = True
        self.od_config = self.load_yaml('od_config.yaml')['order']
        self.date = (date.today() - timedelta(days=1)).isoformat()
        self.saveDataDir = Path(os.getcwd()).parent.joinpath('data')

    @staticmethod
    def login():
        lg = bs.login()
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)

    def saveToDB(self, fn, cols_name, data, update_date=''):
        if self.isSaveToLocal:
            FileUtils.save_pd_csv(self.saveDataDir.joinpath(fn + '.csv').as_posix(), cols_name, data)
        if self.isSaveToMysql:
            self.push(fn, cols_name, data, update_date)

    def getAllStock(self):
        BsUtils.login()
        rs = bs.query_all_stock(self.date)
        print('query_all_stock respond error_code:' + rs.error_code)
        print('query_all_stock respond  error_msg:' + rs.error_msg)
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        bs.logout()
        self.saveToDB('all_stock_code', rs.fields, data, self.date)
        return data, rs.fields

    def getHistKData(self, code, frequency='d', adjustFlag='3'):
        BsUtils.login()
        rs = bs.query_history_k_data_plus(
            code,
            self.od_config['histK'][frequency],
            start_date='1990-12-19',
            end_date=self.date,
            frequency=str(frequency),
            adjustflag=adjustFlag
        )
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        bs.logout()
        self.saveToDB('all_history_k', rs.fields, data, self.date)
        return data, rs.fields

    def getAllHistData(self):
        all_stock = self.get(tableName='all_stock_code', whereCondition="update_date='{}'".format(self.date))
        all_stock = [s['code'] for s in all_stock]
        if len(all_stock) == 0:
            all_stock, colsName = self.getAllStock()
        for stock_code in all_stock:
            for frequency in self.od_config['histK']:
                for ad in ["1", "2", "3"]:
                    print('+ Get stock: {}, frequency: {}, adjustFlag: {}'.format(stock_code, frequency, ad))
                    self.getHistKData(stock_code, frequency, ad)


if __name__ == '__main__':
    bu = BsUtils()
    # bu.getAllStock()
    bu.getAllHistData()