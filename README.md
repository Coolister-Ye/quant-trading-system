# quant-trading-system
Quant trading system which enables auto trading in Chinese market using TONGHUASHUN(THS) app, which naturally support most of 
the commonly used broker. The Auto order code has been tested on THS (version 2.3.1-(4.6.13) MAC). Most of the functionality
run on the gui and application level, implemented mainly by "atomacos" and "pyautogui", avoiding hacking into the lower level
of the app.

### Versions
- v1.0: AutoOrder.py (Using PA Broker App to automate the trading and just support only one broker.)
- v1.1: AutoOrderThs.py (Using THS app to automate the trading and support several broker in the market.)

### Functionality
- quant-trading-system
    - AutoTradingService (Auto trading and Monitor function)
    - config (Database and App info configuration)
    - crontab (Save historical data to local database sh file)
    - utils (Toolbox)
    