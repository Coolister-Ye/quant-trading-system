import re
import time
import logging
import atomacos
import numpy as np
import pyautogui
import atomacos.errors
from utils.FileUtils import FileUtils


class AutoOrderThs(FileUtils):
    def __init__(self):
        super().__init__()
        logging.info('@ Start Auto Order (THS) Service ... ')
        self.config = self.load_yaml('od_config.yaml')['order']['tongHuaShun']
        self.app, self.window = self.activate()

    def activate(self):
        atomacos.launchAppByBundleId(self.config['appId'])
        app = atomacos.getAppRefByBundleId(self.config['appId'])
        window = app.windows()[0]
        return app, window

    def setDirection(self, direction='buy'):
        direction_bt = self.window.buttons(self.config['direction'][direction])[0]
        direction_bt.Press()

    @staticmethod
    def checkCode(stock_code):
        if re.match('[0-9]+$', stock_code) is None:
            logging.error('SocketCode can contain number only: ', stock_code)
            raise ValueError
        elif len(stock_code) != 6:
            logging.error('SocketCode should be length of 6: ', stock_code)
            raise ValueError
        return True

    @staticmethod
    def checkPrice(price, lowest_price, highest_price):
        if price < lowest_price or price > highest_price:
            logging.error(
                'Socket Price should between {} and {}, but with {}'.format(str(lowest_price), str(highest_price),
                                                                            str(price)))
            raise ValueError
        return True

    @staticmethod
    def checkQuantity(quantity, available_quantity):
        if quantity > available_quantity or quantity <= 0:
            logging.error(
                'Quantity Invalid, not in available range [0-{}]: {}'.format(available_quantity, quantity))
            raise ValueError
        elif quantity % 100 > 0:
            logging.error(
                'Quantity Invalid, cannot totally divide by 100: ' + str(quantity))
            raise ValueError
        return True

    @staticmethod
    def setCode(code, code_tf):
        code_tf.AXFocused = "True"
        pyautogui.write(code, interval=0.1)
        code_tf.AXValue = code

    def setPrice(self, price, price_tf):
        """
        Set price to buy or sell
        :param price: 'lowest', 'highest', 'auto' or numerical input;
        numerical input: if input less than 0, price will set to auto price - input
        :param price_tf: AX text fields
        :return:
        """
        lowest_bt = self.window.findFirst(AXIdentifier='_NS:49')
        highest_bt = self.window.findFirst(AXIdentifier='_NS:63')
        lowest_price = lowest_bt.AXTitle
        highest_price = highest_bt.AXTitle

        if price == 'lowest':
            lowest_bt.Press()
        elif price == 'highest':
            highest_bt.Press()
        elif price == 'auto':
            print('@ Auto Price: ', price_tf.AXValue)
        elif price < 0 and AutoOrderThs.checkPrice(float(price_tf.AXValue) - price, lowest_price, highest_price):
            print('@ Auto Price with delta-{}: {}'.format(price, float(price_tf.AXValue) - price))
            price_tf.AXValue = str(price)
        elif AutoOrderThs.checkPrice(price, lowest_price, highest_price):
            print('@ Manual Price with delta-{}: {}'.format(price, float(price_tf.AXValue) - price))
            price_tf.AXValue = str(price)

    def setQuantity(self, quantity, quantity_tf):
        """
        Set Quantity to buy or sell
        :param quantity: 'all': buy or sell all available quantity;
        if quantity between 0 and 1, action on percentage of all available quantity;
        :param quantity_tf: AX text fields
        :return:
        """
        available_bt = self.window.findFirst(AXIdentifier='_NS:71')
        available_txt = available_bt.AXTitle
        available_quantity = int(available_txt.split(':')[-1][:-1])
        if available_quantity == 0:
            logging.error(
                'Available Quantity is zero')
            raise ValueError
        elif quantity == 'all':
            available_bt.Press()
        elif 1 > quantity > 0 and available_quantity > 0:
            quantity = max(np.floor(available_quantity / 100 * quantity) * 100, available_quantity)
            quantity_tf.AXValue = str(quantity)
        elif AutoOrderThs.checkQuantity(quantity, available_quantity):
            quantity_tf.AXValue = str(quantity)

    def setStockInfo(self, stock_code, price, quantity):
        if AutoOrderThs.checkCode(stock_code):
            price_tf, code_tf, quantity_tf = self.window.textFields()
            AutoOrderThs.setCode(stock_code, code_tf)
            self.setPrice(price, price_tf)
            self.setQuantity(quantity, quantity_tf)

    def confirm(self, direction='buy', is_confirm=True):
        confirm_txt = self.config['confirm'] + self.config['direction'][direction]
        confirm_bt = self.window.buttons(confirm_txt)[0]
        confirm_bt.Press()
        confirm_sheet = self.window.sheets()[0]
        confirm_info = confirm_sheet.staticTexts()[1].AXValue
        yes_bt, no_bt = confirm_sheet.buttons()
        if is_confirm:
            yes_bt.Press()
        else:
            no_bt.Press()

        confirm_info = confirm_info.split('\n')[:-3]
        print('@ Confirm info: ', confirm_info)

    def order(self, direction, stock_code, price, quantity, is_confirm=True):
        """
        Auto order interface
        :param is_confirm: True (Action), False (Test)
        :param direction: 'buy' or 'sell'
        :param stock_code: ie: '888888'
        :param price: 'lowest', 'highest', 'auto' or numerical input;
        numerical input: if input less than 0, price will set to auto price - input
        :param quantity: 'all': buy or sell all available quantity;
        if quantity between 0 and 1, action on percentage of all available quantity;
        :return:
        """
        self.setDirection(direction)
        self.setStockInfo(stock_code, price, quantity)
        self.confirm(direction, is_confirm)

    def cancel(self, stock_code='all'):
        ordered_bt = self.window.buttons(self.config['cancel']['tab'])[0]
        ordered_bt.Press()
        scroller = self.window.findFirst(AXIdentifier='_NS:107')
        ordered_table = scroller.findFirst(AXRole='AXTable')
        ordered_fields = ordered_table.findFirstR(AXRole='AXStaticText', AXValue=stock_code)
        if ordered_fields is None:
            return True
        else:
            pyautogui.click(ordered_fields.AXPosition)
            pyautogui.doubleClick(ordered_fields.AXPosition)
            confirm_sheet = self.window.sheets()[0]
            yes_bt, no_bt = confirm_sheet.buttons()
            yes_bt.Press()
            time.sleep(3)
            self.cancel(stock_code)


if __name__ == '__main__':
    aot = AutoOrderThs()
    for i in range(10):
        aot.order('buy', '600789', 'auto', 100, is_confirm=True)
    aot.cancel('600789')
