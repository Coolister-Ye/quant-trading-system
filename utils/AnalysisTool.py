import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, find_peaks_cwt


class AnalysisTool:
    def __init__(self):
        pass

    @staticmethod
    def getClosePrice(KData):
        KData = sorted(KData, key=lambda k: k['day'])
        closePriceData = [float(k['close']) for k in KData]
        date = [k['day'] for k in KData]
        return np.array(closePriceData), np.array(date)

    @staticmethod
    def movingAverage(data, length=5):
        res = np.cumsum(np.insert(data, 0, 0))
        res = (res[length:] - res[:-length]) / length
        return np.insert(res, 0, [data[0]] * (length - 2))

    @staticmethod
    def findPeakAndDip(tsData, isCwt=False):
        tsDataInverse = -tsData
        if isCwt:
            peaks = find_peaks_cwt(tsData, np.arange(1, 10))
            dips = find_peaks_cwt(tsDataInverse, np.arange(1, 10))
        else:
            peaks, _ = find_peaks(tsData, distance=5, prominence=0.1)
            dips, _ = find_peaks(tsDataInverse, distance=5, prominence=0.1)
        return peaks, dips

    @staticmethod
    def plotData(tsData, peaks, dips, ma):
        plt.plot(tsData)
        plt.plot(peaks, tsData[peaks], 'x')
        plt.plot(dips, tsData[dips], 'gx')
        for m in ma:
            plt.plot(m)
        plt.show()
