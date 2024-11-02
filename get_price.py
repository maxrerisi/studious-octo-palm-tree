import yfinance as yf


def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period="1d")
    if not stock_info.empty:
        return stock_info['Close'].iloc[-1]
    else:
        return None


if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol: ")
    price = get_stock_price(ticker)
    if price:
        print(f"The current price of {ticker} is ${price:.2f}")
    else:
        print(f"Could not retrieve the price for {ticker}")
