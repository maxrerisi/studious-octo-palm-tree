from manage_times import current_time, time_to_text, other_time_to_arrow
import json
from stock_data import get_stock_price, get_updates
import yfinance as yf
import arrow


class Transaction():
    def __init__(self, amt: int, ticker: str, sold: bool) -> None:
        self.shares = amt
        self.time = current_time()
        self.last_update = self.time()
        self.ticker = ticker
        # will assume every transaction is a buy, and you can only sell what you have bought
        self.sell = sell
        self.price = get_stock_price(self.ticker)
        self.total = self.shares * self.price
        self.events = []

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self) -> str:
        return f"{'Sold' if self.sell else 'Bought'} {self.shares} shares of {self.ticker} {time_to_text(self.time)}"

    def __dict__(self):
        return {
            "amount": self.shares,
            "time": self.time,
            "ticker": self.ticker,
            "sell": self.sell,
            "price": self.price,
            "total": self.total,
            "events": self.events
        }

    def check_events(self):
        if not self.sell:
            updates = get_updates(self.ticker, self.last_update)
            self.last_update = current_time()
            for event in updates:
                event['collected'] = False
                self.events.append(event)
            self.collect_splits()

    def collect_splits(self):
        if not self.sell:
            for event in self.events:
                if event['type'] == 'split' and not event['collected']:
                    self.shares *= event['amount']
                    self.total = self.shares * self.price
                    event['collected'] = True

    def collect_dividends(self):
        if not self.sell:
            out = 0
            for event in self.events:
                if event['type'] == 'dividend' and not event['collected']:
                    out += event['amount'] * self.shares
                    event['collected'] = True
            return out
        return None

    def sell(self):
        self.sell = True
        self.sell_time = current_time()
        return self.co
