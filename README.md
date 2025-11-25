# market_data

This repository contains automated pipelines for collecting and processing financial market data across three domains: equities, cryptocurrencies, and commodities.
Playwright is used for dynamic web scraping, while Yahoo Finance provides historical OHLCV price data.


## Project Structure
```bash
market_data/
│
├── stocks/
│   ├── get_tickers.py
│   ├── stocks.ipynb
│   ├── tickers/                (gitignored)
│   ├── stocks_info/            (gitignored)
│   └── stocks_price_data/      (gitignored)
│
├── crypto/
│   ├── get_tickers.py
│   ├── crypto.ipynb
│   ├── tickers/                (gitignored)
│   └── crypto_price_data/      (gitignored)
│
├── commodities/
│   ├── get_tickers.py
│   ├── commodities.ipynb
│   ├── tickers/                (gitignored)
│   ├── commodities_info/       (gitignored)
│   └── commodities_price_data/ (gitignored)
│
├── .gitignore
├── requirements.txt
└── README.md
```


## Features

### 1. Ticker Collection

Each module provides a get_tickers.py scraper that:
- Loads dynamic pages using Playwright
- Extracts available ticker symbols
- Saves them into tickers/*.csv

### 2. Historical Price Download

Each notebook includes functions such as:

```python
download_index_prices(index_name, csv_path, limit=10, start_date="auto", end_date="auto")
download_crypto_prices(...)
```

These download OHLCV data from Yahoo Finance based on collected tickers.

### 3. Data Cleaning

Each notebook includes a cleaning function that:
- Normalizes column names
- Ensures valid timestamps
- Converts numeric columns
- Fixes misformatted export files

### 4. Visualization

Helper functions (e.g., plot_stock) generate candlestick charts using mplfinance.


## Installation

Create and activate your environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install playwright
playwright install
```


## Usage

### 1. Collect Tickers

```bash
python3 stocks/get_tickers.py
python3 crypto/get_tickers.py
python3 commodities/get_tickers.py
```

CSV files will appear under each module’s tickers/ folder.


### 2. Download Price Data

Run the relevant notebook:
- stocks/stocks.ipynb
- crypto/crypto.ipynb
- commodities/commodities.ipynb

Each notebook:
- Loads tickers
- Downloads OHLCV data
- Optionally fetches asset information (for stocks and commodities)


### 3. Clean the Data

Each notebook includes:

```python
clean_price_folder("stocks_price_data/sp500_stocks")
```

This standardizes the CSV files into:
Date, Open, High, Low, Close, Volume.


### 4. Plot an Asset

Example:

```python
plot_stock("stocks_price_data/sp500_stocks/AAPL.csv", "AAPL", period_days=180)
```


## Requirements
- Python 3.10+
- Playwright
- pandas
- yfinance
- tqdm
- mplfinance


## Notes
- playwright install must be run after dependency installation.
- All large data directories are gitignored.