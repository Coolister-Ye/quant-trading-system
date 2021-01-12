import time
import random
import logging
import atomacos
from threading import Thread
from utils.FileUtils import FileUtils


class AutoRefresh(Thread):
    def __init__(self):
        super().__init__()
        logging.info('@ Start Auto Refresh Service ... ')
        fu = FileUtils()
        self.config = fu.load_yaml('od_config.yaml')['order']
        self.app = atomacos.getAppRefByBundleId(self.config['appId'])
        self.window = self.app.windows()[0]
        self.button = self.window.buttons(self.config['defaultCheckBoxTitle'])[0]

    def clickCheckBox(self, mainWindow, titleName=''):
        axTitle = self.config['defaultCheckBoxTitle'] if titleName == '' else titleName
        checkBox = mainWindow.findFirst(AXRole='AXCheckBox', AXTitle=axTitle)
        checkBox.Press()

    def run(self):
        try:
            logging.debug('Auto Refresh')
            self.button.Press()
        except:
            logging.warning('Cannot refresh: App conflict')
        time.sleep(random.randint(60, 240))
        self.run()


if __name__ == '__main__':
    ar = AutoRefresh()
    ar.run()
