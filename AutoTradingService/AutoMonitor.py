import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.BsUtils import BsUtils
from utils.AnalysisTool import AnalysisTool


class AutoMonitor(BsUtils, AnalysisTool):
    def __init__(self):
        super().__init__()

    def monitorStock(self, stock_code):
        daily_close_price = pd.DataFrame(self.getDailyStockData(stock_code=stock_code, adjust_flag='2'))
        daily_close_price = daily_close_price[daily_close_price['date'] >= '2020-01-01']
        daily_close_price = np.array([float(i) for i in daily_close_price['close'].values])
        daily_peaks, daily_dips = self.findPeakAndDip(daily_close_price, isCwt=False)
        daily_ma_10 = self.movingAverage(daily_close_price, length=20)
        self.plotData(daily_close_price, daily_peaks, daily_dips, [daily_ma_10])


if __name__ == '__main__':
    autoM = AutoMonitor()
    autoM.monitorStock('sh.600400')
