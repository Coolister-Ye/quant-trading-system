import re
import requests
from utils.FileUtils import FileUtils
import matplotlib.pyplot as plt
from utils.AnalysisTool import AnalysisTool


class SianaUtils(FileUtils, AnalysisTool):
    def __init__(self):
        super().__init__()
        self.config = self.load_yaml('od_config.yaml')['realTime']['sina']

    def getRealTimeData(self, stockCode):
        r = requests.get(self.config['RealTimeUrl'] + stockCode)
        if r.status_code == 200:
            res = re.sub(r'"', '', r.text).split('=')[1]
            res = dict(zip(self.config['colName'], res.split(',')))
            return res

    def getRealTimeKData(self, stockCode, scale='5', ma='no', dataLen='1023'):
        with requests.Session() as s:
            print(self.config['RealTimeKData'].format(stockCode, scale, ma, dataLen))
            r = s.get(self.config['RealTimeKData'].format(stockCode, scale, ma, dataLen))
            if r.status_code == 200:
                res = eval(r.text.split('=')[2][1:-2])
                return res

    def testCase(self):
        k_data = self.getRealTimeKData('sh601211')
        ts_data, _ = self.getClosePrice(k_data)
        ts_data = ts_data[-500:]
        ps, ds = self.findPeakAndDip(ts_data, False)
        ma_20 = self.movingAverage(ts_data, 20)
        self.plotData(ts_data, ps, ds, [ma_20])


if __name__ == '__main__':
    su = SianaUtils()
    su.testCase()
