import re
import logging
import atomacos
import pyautogui
from utils.FileUtils import FileUtils


class AutoOrder(FileUtils):

    def __init__(self):
        super().__init__()
        logging.info('@ Start Auto Order Service ... ')
        self.config = self.load_yaml('od.config.yaml')['order']

    def activate(self):
        atomacos.launchAppByBundleId(self.config['appId'])
        app = atomacos.getAppRefByBundleId(self.config['appId'])
        return app

    def clickCheckBox(self, mainWindow, titleName=''):
        axTitle = self.config['defaultCheckBoxTitle'] if titleName == '' else titleName
        checkBox = mainWindow.findFirst(AXRole='AXCheckBox', AXTitle=axTitle)
        checkBox.Press()

    @staticmethod
    def clickComboBox(ComboBox, itemIndex=0):
        CodeButton = ComboBox.AXChildren[0]
        CodeButton.clickMouseButtonLeft(CodeButton.AXPosition)
        CodeText = ComboBox.AXChildren[1].AXChildren[0].AXChildren[itemIndex]
        CodeText.clickMouseButtonLeft(CodeText.AXPosition)

    def setMarketCode(self, allComboBox, marketCode='SZ'):
        marketCodeComboBox = allComboBox[0]
        if marketCode in self.config['marketCode']:
            marketCoedIndex = int(self.config['marketCode'][marketCode])
            AutoOrder.clickComboBox(marketCodeComboBox, marketCoedIndex)
        else:
            logging.error("Market Code is invalid: " + marketCode)
            raise ValueError

    @staticmethod
    def checkSocketCodeValid(socketCode):
        if re.match('[0-9]+$', socketCode) is None:
            logging.error('SocketCode can contain number only: ', socketCode)
            raise ValueError
        elif len(socketCode) != 6:
            logging.error('SocketCode should be length of 6: ', socketCode)
            raise ValueError
        return True

    @staticmethod
    def setStockCode(allTextField, socketCode=""):
        AutoOrder.checkSocketCodeValid(socketCode)
        socketCodeText = allTextField[0]
        socketCodeText.AXFocused = True
        pyautogui.write(socketCode, interval=0.1)

    @staticmethod
    def checkPriceWayValid(priceWay):
        if priceWay not in (1, 2, 3, 4, 5):
            logging.error('Price Way should be 1 to 5: ', str(priceWay))
            raise ValueError
        else:
            return True

    @staticmethod
    def setPriceWay(allComboBox, priceWay):
        AutoOrder.checkPriceWayValid(priceWay)
        AutoOrder.clickComboBox(allComboBox[1], priceWay - 1)

    @staticmethod
    def setQuantity(allTextField, allQuantityButton, quantity):
        if quantity <= 0:
            allQuantityButton.Press()
        else:
            allTextField.AXValue = quantity

    def order(self, directionTab, marketCode, socketCode, priceWay=1, quantity=-1, isAction=False):
        app = self.activate()
        mainWindow = app.windows()[0]
        allComboBox = mainWindow.findAll(AXRole='AXComboBox')
        allTextField = mainWindow.textFields()
        allQuantityButton = mainWindow.findFirst(AXRole='AXButton', AXTitle=self.config['allQuantityTitle'])
        actionButton = mainWindow.findFirst(AXRole='AXButton', AXTitle=directionTab + self.config['actionText'])
        self.clickCheckBox(directionTab, mainWindow)
        self.setMarketCode(allComboBox, marketCode)
        AutoOrder.setStockCode(allTextField, socketCode)
        AutoOrder.setPriceWay(allComboBox, priceWay)
        if priceWay == 1:
            AutoOrder.setQuantity(allTextField, allQuantityButton, quantity)
        if isAction:
            actionButton.Press()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    ao = AutoOrder()