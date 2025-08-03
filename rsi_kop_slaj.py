import yfinance as yf
import pandas as pd
import ta
from ta.momentum import RSIIndicator

# Hämta data för Investor B
data = yf.download("INVE-B.ST", start="2024-01-01", end="2025-01-01")
# Skapa RSI-objekt med fönster på 14 dagar
rsi = RSIIndicator(close=data['Close'], window=14)

# Lägg till RSI till DataFrame
#data['RSI'] = rsi.rsi()

data['RSI'] = rsi.rsi().flatten()

# Ta bort rader med Na


# Köp/sälj baserat på RSI
data['Signal'] = 0
data.loc[data['RSI'] < 30, 'Signal'] = 1  # Köp
data.loc[data['RSI'] > 70, 'Signal'] = -1 # Sälj

print(data[['Close', 'RSI', 'Signal']].tail(20))
