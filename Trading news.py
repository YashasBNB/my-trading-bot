import MetaTrader5 as mt5

# Initialize MetaTrader 5
if not mt5.initialize():
    print("MetaTrader5 initialization failed")
    quit()

# Replace with your demo account number and password
account = 86342017  # Replace with your actual demo account number
password = "3@BdTaVs"  # Replace with the actual password
server = "MetaQuotes-Demo"  # Demo server for MetaTrader5

# Log in to the demo account
if not mt5.login(account, password, server):
    print(f"Failed to connect. Error code: {mt5.last_error()}")
    mt5.shutdown()
    quit()

# Get all available symbols
symbols = mt5.symbols_get()
if not symbols:
    print("Failed to get symbols.")
    mt5.shutdown()
    quit()

# Print the first 10 symbols
for symbol in symbols[:10]:
    print(symbol.name)

# Select a specific symbol, for example EURUSD
symbol = "EURUSD"
if not mt5.symbol_select(symbol, True):
    print(f"Failed to select {symbol}")
    mt5.shutdown()
    quit()

# Get tick data for the symbol
ticks = mt5.symbol_info_tick(symbol)
if not ticks:
    print(f"Failed to retrieve tick data for {symbol}")
    mt5.shutdown()
    quit()

print(f"Bid: {ticks.bid}, Ask: {ticks.ask}, Last: {ticks.last}")

# Define the trade request
trade_request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": 0.01,  # Adjusted volume (check broker’s requirements)
    "type": mt5.ORDER_TYPE_BUY,
    "price": ticks.ask,  # The price to buy at
    "sl": ticks.ask - 0.01,  # Adjust Stop Loss
    "tp": ticks.ask + 0.01,  # Adjust Take Profit
    "deviation": 10,  # Adjusted deviation (check broker’s requirements)
    "magic": 234000,  # Magic number to identify your orders
    "comment": "Trade from Python",
    "type_time": mt5.ORDER_TIME_GTC,  # Good till canceled
    "type_filling": mt5.ORDER_FILLING_IOC,
}

# Send the trade request
result = mt5.order_send(trade_request)
if result.retcode == mt5.TRADE_RETCODE_DONE:
    print("Trade executed successfully")
else:
    print(f"Trade failed. Error code: {result.retcode}, Error description: {mt5.last_error()}")

# Shutdown MetaTrader 5
mt5.shutdown()
