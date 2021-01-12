import os
import pandas as pd
import baostock as bs
from pathlib import Path
from utils.FileUtils import FileUtils
from utils.DbUtils import DbUtils
from datetime import date, timedelta


class BsUtils(DbUtils, FileUtils):

    def __init__(self):
        super().__init__()
        self.isSaveToLocal = False
        self.isSaveToMysql = True
        self.od_config = self.load_yaml('od_config.yaml')['baoStock']
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
        rs_detail = bs.query_stock_basic()
        print('query_all_stock respond error_code:' + rs.error_code)
        print('query_all_stock respond  error_msg:' + rs.error_msg)
        print('query_stock_basic respond error_code:' + rs_detail.error_code)
        print('query_stock_basic respond  error_msg:' + rs_detail.error_msg)
        data, data_detail = [], []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        while (rs_detail.error_code == '0') & rs_detail.next():
            data_detail.append(rs_detail.get_row_data())
        bs.logout()
        self.saveToDB('all_stock_code', rs.fields, data, self.date)
        self.saveToDB('all_stock_basic', rs_detail.fields, data_detail, self.date)
        return data, rs.fields

    def getHistKData(self, code, frequency='d', adjustFlag='3', retry=0, start_date='1992-01-01'):
        rs = bs.query_history_k_data_plus(
            code,
            self.od_config['histK'][frequency],
            start_date=start_date,
            end_date=self.date,
            frequency=str(frequency),
            adjustflag=adjustFlag
        )
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        if retry == 2:
            print('- Fail to get {}'.format(code))
        elif len(data) == 0:
            self.getHistKData(code, frequency=frequency, adjustFlag=adjustFlag, retry=retry+1)
        else:
            self.saveToDB('all_daily_history_k', rs.fields, data, self.date)
        return data, rs.fields

    def getAllHistData(self, start_date=None):
        all_stock_basic = pd.DataFrame(self.get(tableName='all_stock_basic', whereCondition="update_date='{}'".format(self.date)))
        all_stock = all_stock_basic[(all_stock_basic['type'] == '1') & (all_stock_basic['status'] == '1')]
        all_stock = [s[0] for s in all_stock.values]
        start_date = self.date if start_date is None else start_date
        if len(all_stock) == 0:
            all_stock, colsName = self.getAllStock()
        for stock_code in all_stock:
            for frequency in self.od_config['histK']:
                for ad in ["2", "3"]:
                    print('+ Get stock: {}, frequency: {}, adjustFlag: {}'.format(stock_code, frequency, ad))
                    self.getHistKData(stock_code, frequency, ad, start_date=start_date)

    def getDailyStockData(self, stock_code, adjust_flag="3"):
        data = self.get(tableName='all_daily_history_k', whereCondition="code='{}' and adjustFlag='{}'".format(stock_code, adjust_flag))
        return data


if __name__ == '__main__':
    bu = BsUtils()
    bu.getAllStock()
    BsUtils.login()
    bu.getAllHistData()
    bs.logout()
