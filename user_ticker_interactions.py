from manage_times import current_time, time_to_text
import json
from stock_data import get_stock_price, get_updates


class UserTickerInteraction:
    def __init__(self, user_id: int, ticker: str) -> None:
        self.user_id = user_id
        self.ticker = ticker
        self.time = current_time()
        self.last_update = self.time
        self.total_shares = 0
        self.transactions = []
        self.events = []

    def add_transaction(self, amt: int, sell: bool) -> None:
        price = get_stock_price(self.ticker)
        transaction = {
            "amount": amt,
            "time": current_time(),
            "sold": sell,
            "price": get_stock_price(self.ticker),
            "total": amt * price
        }
        self.transactions.append(transaction)
        self.total_shares += -amt if sell else amt

    def to_json(self):
        return json.dumps(self.__dict__())

    def __str__(self) -> str:
        return f"User {self.user_id} {'Sold' if self.total_shares < 0 else 'Bought'} {abs(self.total_shares)} shares of {self.ticker} {time_to_text(self.time)}"

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "ticker": self.ticker,
            "time": self.time,
            "last_update": self.last_update,
            "total_shares": self.total_shares,
            "transactions": self.transactions,
            "events": self.events
        }

    def check_events(self):
        updates = get_updates(self.ticker, self.last_update)
        self.last_update = current_time()
        for event in updates:
            event['collected'] = False
            self.events.append(event)
        self.collect_splits()

    def collect_splits(self):
        for event in self.events:
            if event['type'] == 'split' and not event['collected']:
                self.total_shares *= event['amount']
                event['collected'] = True

    def collect_dividends(self):
        out = 0
        for event in self.events:
            if event['type'] == 'dividend' and not event['collected']:
                out += event['amount'] * self.total_shares
                event['collected'] = True
        return out if out > 0 else None
