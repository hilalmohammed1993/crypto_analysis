import sys
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from analysis import market, news

def main():
    parser = argparse.ArgumentParser(description="Crypto Analyst Tool")
    parser.add_argument("symbol", help="Ticker symbol (e.g., BTC-USD, ETH-USD)")
    args = parser.parse_args()
    
    symbol = args.symbol.upper()
    if not symbol.endswith("-USD") and "-" not in symbol:
        symbol += "-USD"
        
    console = Console()
    console.print(f"[bold blue]Analyzing {symbol}...[/bold blue]")
    
    # 1. Market Data & Trend
    try:
        df = market.fetch_data(symbol)
        current_price = df['Close'].iloc[-1]
        
        support, resistance = market.calculate_support_resistance(df)
        trend, sma50, sma200 = market.analyze_trend(df)
        
        market_table = Table(title=f"Market Analysis: {symbol}")
        market_table.add_column("Metric", style="cyan")
        market_table.add_column("Value", style="magenta")
        
        market_table.add_row("Current Price", f"${current_price:,.2f}")
        market_table.add_row("Trend", trend)
        market_table.add_row("Support (Recent)", f"${support:,.2f}")
        market_table.add_row("Resistance (Recent)", f"${resistance:,.2f}")
        market_table.add_row("SMA50", f"${sma50:,.2f}")
        market_table.add_row("SMA200", f"${sma200:,.2f}")
        
        console.print(market_table)
        
    except Exception as e:
        console.print(f"[bold red]Error analyzing market data: {e}[/bold red]")
        return

    # 2. News Analysis
    console.print(f"\n[bold blue]Fetching News for {symbol}...[/bold blue]")
    try:
        # Search query clean up (remove -USD)
        query = symbol.replace("-USD", "")
        articles = news.fetch_news(query)
        
        if not articles:
            console.print("No recent news found.")
        else:
            for article in articles:
                sentiment, polarity = news.analyze_sentiment(article['title'])
                
                color = "green" if sentiment == "Positive" else "red" if sentiment == "Negative" else "yellow"
                
                news_panel = Panel(
                    Text(f"Title: {article['title']}\nPublished: {article['pub_date']}\nSentiment: {sentiment} ({polarity:.2f})", style="white"),
                    title=f"[link={article['link']}]Read Article[/link]",
                    border_style=color
                )
                console.print(news_panel)
                
    except Exception as e:
        console.print(f"[bold red]Error fetching news: {e}[/bold red]")

if __name__ == "__main__":
    main()
