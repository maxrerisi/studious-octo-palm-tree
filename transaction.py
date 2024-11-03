from manage_times import current_time, time_to_text, other_time_to_arrow
import json
from stock_data import get_stock_price
import yfinance as yf
import arrow


class Transaction():
    def __init__(self, amt: int, ticker: str, sell: bool) -> None:
        self.amount = amt
        self.time = current_time()
        self.last_update = self.time()
        self.ticker = ticker
        self.sell = sell
        self.price = get_stock_price(self.ticker)
        self.total = self.amount * self.price
        self.events = []

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self) -> str:
        return f"{'Sold' if self.sell else 'Bought'} {self.amount} shares of {self.ticker} {time_to_text(self.time)}"

    def __dict__(self):
        return {
            "amount": self.amount,
            "time": self.time,
            "ticker": self.ticker,
            "sell": self.sell,
            "price": self.price,
            "total": self.total
        }

    def check_events(self):
        stock = yf.Ticker(self.ticker)
        events = stock.history(start=self.last_update, end=current_time())

        if not events.empty:
            print(f"New events for {self.ticker} since last update:")
            print(events)
        self.last_update = current_time()


stock = yf.Ticker('msft')
print(time_to_text(
    stock.dividends.index[0]), stock.dividends.iloc[0])
print(stock.dividends)
input()
events = stock.history(start=arrow.Arrow(2020, 10, 1), end=current_time())

if not events.empty:
    print(f"New events for {'msft'} since last update:")
    print(events)
    for ev in events.iloc():
        if ev['Dividends'] > 0:
            print(f"Dividend of {ev['Dividends']} on {ev.name}")
