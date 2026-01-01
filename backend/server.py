from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from analysis import market, news
import uvicorn

app = FastAPI(title="Crypto Analyst API")

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")

# Allow CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ideally restrictive in prod, but fine for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analysis/{symbol}")
def get_analysis_data(symbol: str):
    """
    Returns full analysis for a given coin.
    """
    symbol = symbol.upper()
    
    # 1. Market Data Analysis
    try:
        df = market.fetch_data(symbol)
        current_price = df['Close'].iloc[-1]
        
        support, resistance = market.calculate_support_resistance(df)
        trend, sma50, sma200 = market.analyze_trend(df)
        rsi_val, rsi_signal = market.calculate_rsi(df)
        vol_val, vol_sma, vol_status = market.analyze_volume(df)
        
        market_data = {
            "price": current_price,
            "trend": {
                "status": trend,
                "sma50": sma50,
                "sma200": sma200
            },
            "support_resistance": {
                "support": support,
                "resistance": resistance
            },
            "indicators": {
                "rsi": {
                    "value": rsi_val,
                    "signal": rsi_signal
                },
                "volume": {
                    "current": vol_val,
                    "sma": vol_sma,
                    "status": vol_status
                }
            },
            "history": df.tail(90).reset_index().apply(
                lambda x: {"date": x['Date'].strftime('%Y-%m-%d'), "price": x['Close']}, axis=1
            ).tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Market data error: {str(e)}")

    # 2. News Analysis
    try:
        # HBAR-USD -> HBAR
        query_symbol = symbol.split("-")[0] if "-" in symbol else symbol
        articles = news.fetch_news(query_symbol)
        analyzed_news = []
        for article in articles:
            sentiment, polarity = news.analyze_sentiment(article['title'])
            analyzed_news.append({
                "title": article['title'],
                "link": article['link'],
                "pub_date": article['pub_date'],
                "sentiment": sentiment,
                "polarity": polarity
            })
    except Exception as e:
        analyzed_news = [] # Fail gracefully for news

    return {
        "symbol": symbol,
        "market_analysis": market_data,
        "news": analyzed_news
    }

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
