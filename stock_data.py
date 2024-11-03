import yfinance as yf
from manage_times import current_time, other_time_to_arrow, time_to_text
import arrow


def get_stock_price(ticker, amt=1):
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period="1d")
    if not stock_info.empty:
        return stock_info['Close'].iloc[-1] * amt
    else:
        return None


def get_updates(ticker, start, end=current_time()):
    stock = yf.Ticker(ticker)
    events = stock.history(start=start, end=end)
    out = []
    if events.empty:
        return out
    for date, div in zip(stock.dividends.index, stock.dividends):
        if date.isbetween(start, end):
            out.append({"type": "dividend",
                        "date": other_time_to_arrow(date), "amount": div})
    for date, split in zip(stock.splits.index, stock.splits):
        if date.isbetween(start, end):
            out.append({"type": "split",
                        "date": other_time_to_arrow(date), "amount": split})
    return out


if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol: ")
    price = get_stock_price(ticker)
    if price:
        print(f"The current price of {ticker} is ${price:.2f}")
    else:
        print(f"Could not retrieve the price for {ticker}")
