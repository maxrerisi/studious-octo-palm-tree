from manage_times import current_time, time_to_text, time_for_json
import json
from stock_data import get_stock_price, get_updates


class UserTickerInteraction:
    def __init__(self, user_id: int, ticker: str) -> None:
        self.user_id = user_id
        self.ticker = ticker.upper()
        self.initialize_time = current_time()
        self.last_update = self.initialize_time
        self.total_shares = 0
        self.transactions = []
        self.events = []
        self.uncollected_dividends = 0

    def add_transaction(self, amt: int, sell: bool, price=None) -> None:
        self.gather_uncollected_dividends()
        self.collect_splits()
        if price is None:
            price = get_stock_price(self.ticker)
        if sell and self.total_shares < amt:
            raise ValueError("Cannot sell more shares than you own")
        transaction = {
            "amount": amt,
            "time": time_for_json(current_time()),
            "sold": sell,
            "price": price,
            "total": amt * price
        }
        self.transactions.append(transaction)
        self.total_shares += -amt if sell else amt

    def to_json(self):
        return json.dumps(self.__dict__())

    def __str__(self) -> str:
        return f"User {self.user_id} {'Sold' if self.total_shares < 0 else 'Bought'} {abs(self.total_shares)} shares of {self.ticker} {time_to_text(self.initialize_time)}"

    def events_for_json(self):
        out = []
        e_dict = self.events.copy()
        for e in e_dict:
            e['date'] = time_for_json(e['date'])
            out.append(e)
        return out

    def __dict__(self):
        return {
            "user_id": self.user_id,
            "ticker": self.ticker,
            "time": time_for_json(self.initialize_time),
            "last_update": time_for_json(self.last_update),
            "total_shares": self.total_shares,
            "transactions": self.transactions,
            "events": self.events_for_json()
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

    def gather_uncollected_dividends(self):
        for event in self.events:
            if event['type'] == 'dividend' and not event['collected']:
                self.uncollected_dividends += event['amount'] * \
                    self.total_shares
                event['collected'] = True

    def collect_dividends(self):
        self.gather_uncollected_dividends()
        temp = self.uncollected_dividends
        self.uncollected_dividends = 0
        return temp
