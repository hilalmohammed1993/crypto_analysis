# Crypto Analyst 🚀

A comprehensive cryptocurrency analysis tool that provides real-time market insights and sentiment analysis from global news sources. This project features both a powerful CLI interface and a modern Web Dashboard.

## ✨ Features

- **Market Trend Analysis**: Automatically calculates SMA50 and SMA200 to detect "Golden Cross" or "Death Cross" scenarios.
- **Support & Resistance**: Naive local maxima/minima detection to identify key price levels.
- **Sentiment Analysis**: Fetches the latest global news regarding a specific coin and analyzes sentiment (Positive/Negative/Neutral) using Natural Language Processing.
- **Dual Interface**:
  - **CLI**: Fast, rich-text output in your terminal.
  - **Web Dashboard**: Interactive UI served via FastAPI.
- **Multi-Exchange Support**: Powered by CCXT (defaults to Binance) for high-frequency data fetching.

## 🛠 Tech Stack

- **Language**: Python 3.x
- **Backend Framework**: FastAPI & Uvicorn
- **Data Science**: Pandas, NumPy
- **NLP**: TextBlob
- **Web Scraping**: BeautifulSoup4
- **CLI Styling**: Rich
- **Data Provider**: CCXT (Binance) & Google News RSS

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python installed. It's recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Usage

#### **Terminal / CLI Mode**
Get an instant report on any coin:
```bash
python main.py BTC
```

#### **Web UI / Dashboard**
Launch the FastAPI server:
```bash
python backend/server.py
```
Then visit: `http://localhost:8000`

## 📂 Project Structure

- `main.py`: Entry point for the Command Line Interface.
- `backend/`:
  - `server.py`: FastAPI server logic.
  - `static/`: Frontend assets.
- `analysis/`:
  - `market.py`: Logic for trend, SMA, support, and resistance.
  - `news.py`: News scraping and sentiment analysis logic.
- `requirements.txt`: Project dependencies.
- `render.yaml`: Configuration for one-click deployment to Render.com.

## 🔒 License
This project is open-source and available under the MIT License.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your-username/crypto_analyst/issues).

---
*Made with ❤️ for the Crypto Community.*
