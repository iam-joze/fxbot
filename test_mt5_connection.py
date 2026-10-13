import os
import MetaTrader5 as mt5
from dotenv import load_dotenv

#load_dotenv()

#MT5_PATH = os.environ["MT5_PATH"]
#LOGIN = int(os.environ["MT5_LOGIN"])
#PASSWORD = os.environ["MT5_PASSWORD"]
#SERVER = os.environ["MT5_SERVER"]##

if not mt5.initialize():
    print("initialize() failed, error code:", mt5.last_error())
    quit()

print("MT5 version:", mt5.version())

account_info = mt5.account_info()
if account_info is None:
    print("Failed to get account info, error code:", mt5.last_error())
else:
    print("Login:", account_info.login)
    print("Server:", account_info.server)
    print("Balance:", account_info.balance)
    print("Equity:", account_info.equity)
    print("Currency:", account_info.currency)

mt5.shutdown()