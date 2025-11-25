from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os

# Scrape cryptocurrency ticker symbols from TradingView.
def get_tickers(url, output_csv):
    print(f"Loading TradingView: {url}")

    # Determine Yahoo Finance suffix based on exchange
    yahoo_suffix = "-USD"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("table tbody tr", timeout=60000)

        # Click "Load More" button until all rows are loaded
        for i in range(2):
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
        "https://www.tradingview.com/markets/cryptocurrencies/prices-all/"
    ]

    os.makedirs("tickers", exist_ok=True)

    for link in links:
        if "cryptocurrencies" in link:
            output_file = os.path.join("tickers", "crypto_tickers.csv")
        else:
            continue

        get_tickers(link, output_file)