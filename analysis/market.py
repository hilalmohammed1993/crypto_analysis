import ccxt
import pandas as pd
import numpy as np

def fetch_data(symbol, timeframe='1d', limit=365):
    """
    Fetches historical data using CCXT (Binance).
    """
    try:
        exchange = ccxt.binance()
        # Clean symbol: "BTC-USD" -> "BTC/USDT" mapping for Binance
        # Binance primarily uses USDT for pairs.
        clean_symbol = symbol.replace("-USD", "/USDT").replace("-", "/")
        if "/" not in clean_symbol:
            clean_symbol += "/USDT"
            
        ohlcv = exchange.fetch_ohlcv(clean_symbol, timeframe=timeframe, limit=limit)
        
        if not ohlcv:
            raise ValueError(f"No data found for {clean_symbol}")
            
        df = pd.DataFrame(ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
        df.set_index('Date', inplace=True)
        return df
        
    except Exception as e:
        # Fallback or re-raise
        raise ValueError(f"Error fetching data for {symbol}: {e}")

def calculate_support_resistance(df, window=20):
    """
    Calculates support and resistance levels using a simple window-based approach.
    This is a naive implementation looking for local minima/maxima.
    """
    # Simple rolling min/max for basic levels
    df['Support'] = df['Low'].rolling(window=window, center=True).min()
    df['Resistance'] = df['High'].rolling(window=window, center=True).max()
    
    # Get the most recent valid levels
    latest_support = df['Support'].iloc[-window-1:].min()
    latest_resistance = df['Resistance'].iloc[-window-1:].max()
    
    return latest_support, latest_resistance

def analyze_trend(df):
    """
    Analyzes the trend using SMA50 vs SMA200.
    """
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()
    
    current_price = df['Close'].iloc[-1]
    sma50 = df['SMA50'].iloc[-1]
    sma200 = df['SMA200'].iloc[-1]
    
    trend = "Neutral"
    if sma50 > sma200:
        trend = "Bullish (Golden Cross context)"
    elif sma50 < sma200:
        trend = "Bearish (Death Cross context)"
        
    # Finetune with price vs SMA
    if current_price > sma50:
        trend += " | Price above SMA50"
    else:
        trend += " | Price below SMA50"
        
    return trend, sma50, sma200
