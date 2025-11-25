from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os

# Scrape stock ticker symbols from TradingView.
def get_tickers(url, output_csv):
    
    print(f"Loading TradingView: {url}")

    # Determine Yahoo Finance suffix based on exchange
    if "BIST" in url:
        yahoo_suffix = ".IS"
    elif "NSE" in url:
        yahoo_suffix = ".NS"
    elif "SSE" in url:
        yahoo_suffix = ".SS"
    else:
        yahoo_suffix = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("table tbody tr", timeout=60000)

        # Click "Load More" button until all rows are loaded
        while True:
            try:
                load_more_button = page.query_selector('button[data-overflow-tooltip-text="Load More"]')
                if not load_more_button:
                    break
                load_more_button.click()
                print("Load More clicked, loading more rows...")
                time.sleep(2)
            except Exception:
                break

        rows = page.query_selector_all("table tbody tr")
        print(f"Table fully loaded ({len(rows)} rows found).")

        tickers = []
        for row in rows:
            symbol = row.query_selector("a.tickerNameBox-GrtoTeat")
            sym_text = symbol.inner_text().strip() if symbol else ""
            if sym_text:
                tickers.append(sym_text)

        browser.close()

    # Create DataFrame and apply Yahoo format
    df = pd.DataFrame({"Symbol": tickers})
    df["Symbol"] = df["Symbol"].str.replace(".", "-", regex=False) + yahoo_suffix

    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"{len(df)} companies saved → {output_csv}")

    return df


if __name__ == "__main__":
    links = [
        "https://www.tradingview.com/symbols/SPX/components/",
        "https://www.tradingview.com/symbols/DJ-DJI/components/",
        "https://www.tradingview.com/symbols/NASDAQ-NDX/components/",
        "https://www.tradingview.com/symbols/NSE-NIFTY/components/",
        "https://www.tradingview.com/symbols/BIST-XU100/components/",
        "https://www.tradingview.com/symbols/SSE-000001/components/"
    ]

    os.makedirs("tickers", exist_ok=True)

    for link in links:
        if "SPX" in link:
            output_file = "tickers/sp500_tickers.csv"
        elif "DJ-DJI" in link:
            output_file = "tickers/dowjones_tickers.csv"
        elif "NASDAQ-NDX" in link:
            output_file = "tickers/nasdaq100_tickers.csv"
        elif "NSE-NIFTY" in link:
            output_file = "tickers/nifty50_tickers.csv"
        elif "BIST-XU100" in link:
            output_file = "tickers/bist100_tickers.csv"
        elif "SSE-000001" in link:
            output_file = "tickers/sse_tickers.csv"
        else:
            continue

        get_tickers(link, output_file)