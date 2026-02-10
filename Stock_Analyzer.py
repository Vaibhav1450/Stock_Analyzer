
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        company_name = info.get("longName", symbol)
        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")

        if current_price is not None and previous_close is not None:
            change = current_price - previous_close
            pct_change = (change / previous_close) * 100
            daily_change = f"{change:+.2f} ({pct_change:+.2f}%)"
        else:
            daily_change = "N/A"

        return {
            "Company Name": company_name,
            "Current Price": f"{current_price:,.2f}" if current_price is not None else "N/A",
            "Daily Change": daily_change,
        }

    except Exception as e:
        print("Error:", e)
        return None


def plot_stock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="3mo")

        if hist.empty:
            print("No historical data available.")
            return

        hist["MA7"] = hist["Close"].rolling(7).mean()
        hist["MA30"] = hist["Close"].rolling(30).mean()

        plt.figure(figsize= (10,6))
        plt.plot(hist["Close"], label="Close Price")
        plt.plot(hist["MA7"], label="7-Day MA")
        plt.plot(hist["MA30"], label="30-Day MA")

        plt.title(f"{symbol} Stock Price Trend")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)

        plt.show()

    except Exception as e:
        print("Plot error:", e)


print("STOCK PRICE ANALYZER")
print("=" * 40)

while True:
    symbol = input("\nEnter stock symbol (or 'quit'): ").strip().upper()

    if symbol.lower() == "quit":
        print("Goodbye!")
        break

    print(f"Fetching {symbol} data...")

    data = get_stock_data(symbol)

    if data:
        print("\nSTOCK DATA:")
        print(f"Symbol: {symbol}")
        print(f"Company: {data['Company Name']}")
        print(f"Price: {data['Current Price']}")
        print(f"Change: {data['Daily Change']}")

        view_graph = input("View it on a graph? (y/n): ").strip().lower()
        if view_graph == "y":
            plot_stock(symbol)

    else:
        print("Invalid stock symbol or data unavailable.")

    print("=" * 40)