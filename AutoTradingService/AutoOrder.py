import re
import logging
import atomacos
import pyautogui
import atomacos.errors
from utils.FileUtils import FileUtils
from AutoTradingService.AutoRefresh import AutoRefresh


class AutoOrder(FileUtils):

    def __init__(self):
        super().__init__()
        logging.info('@ Start Auto Order Service ... ')
        self.config = self.load_yaml('od_config.yaml')['order']
        self.refresh_service = AutoRefresh()
        self.refresh_service.start()

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
        CodeButton.Press()
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
        socketCodeText.AXSelectedText = socketCode
        socketCodeText.Confirm()

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
    def setPrice(allTextField, price):
        if price <= 0:
            print('@ Trading on original market price')
        else:
            allTextField[2].AXValue = str(price)

    @staticmethod
    def setQuantity(allTextField, allQuantityButton, quantity):
        if quantity <= 0:
            allQuantityButton.clickMouseButtonLeft(allQuantityButton.AXPosition)
        else:
            allTextField[1].AXValue = str(quantity)

    def confirm(self, app, mainWindow, directionTab, isAction):
        try:
            actionButton = mainWindow.findFirst(AXRole='AXButton', AXTitle=directionTab + self.config['actionText'])
            actionButton.clickMouseButtonLeft(actionButton.AXPosition)
        except atomacos.errors.AXErrorCannotComplete:
            logging.info('Action not complete error, cannot find a way to handle this fail')

        dialog = app.windows()[0]
        confirmInfo = dialog.staticTexts()[1]
        logging.info('@' + '|'.join(confirmInfo.AXValue.split('\r')[2:7]))
        actionConfirmName = self.config['confirmAction'][isAction]
        ActionConfirmButton = dialog.buttons(actionConfirmName)[0]
        ActionConfirmButton.Press()

    def order(self, directionTab, marketCode, socketCode, priceWay=1, price=-1, quantity=-1, isAction=False):
        app = self.activate()
        mainWindow = app.windows()[0]
        self.clickCheckBox(mainWindow, directionTab)
        allComboBox = mainWindow.findAll(AXRole='AXComboBox')
        allTextField = mainWindow.textFields()
        allQuantityButton = mainWindow.findFirst(AXRole='AXButton', AXTitle=self.config['allQuantityTitle'])
        self.setMarketCode(allComboBox, marketCode)
        AutoOrder.setStockCode(allTextField, socketCode)
        if priceWay != 1:
            AutoOrder.setPriceWay(allComboBox, priceWay)
        else:
            AutoOrder.setPrice(allTextField, price)
        AutoOrder.setQuantity(allTextField, allQuantityButton, quantity)
        self.confirm(app, mainWindow, directionTab, isAction)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    ao = AutoOrder()
    ao.order('卖出', 'SZ', '002024', price=10, quantity=1, isAction=False)
