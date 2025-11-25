from playwright.sync_api import sync_playwright
import pandas as pd
import os

# Scrape commodity ticker symbols from Yahoo Finance.
def get_tickers(url, output_csv):

    print(f"Loading Yahoo Finance page: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Wait for table rows to load
        page.wait_for_selector('tr[data-testid="data-table-v2-row"]')
        rows = page.query_selector_all('tr[data-testid="data-table-v2-row"]')

        print("Scraping symbols...")

        tickers = []

        for row in rows:
            symbol_cell = row.query_selector('td[data-testid-cell="ticker"]')
            if not symbol_cell:
                continue

            raw_symbol = symbol_cell.inner_text().strip()

            # Remove trailing commas (like "ES=F,")
            clean_symbol = raw_symbol.rstrip(",")

            if clean_symbol:
                tickers.append(clean_symbol)

        browser.close()

    # Create DataFrame with ONLY Symbol column
    df = pd.DataFrame({"Symbol": tickers})

    # Save CSV
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} commodity symbols → {output_csv}")

    return df


if __name__ == "__main__":
    url = "https://finance.yahoo.com/markets/commodities/"
    output_csv = "tickers/commodity_tickers.csv"

    os.makedirs("tickers", exist_ok=True)
    get_tickers(url, output_csv)