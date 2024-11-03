from manage_times import current_time
from global_settings import PORTFOLIO_ID_FILE
import json
from stock_data import get_stock_price
from user_ticker_interactions import UserTickerInteraction

# TODO will have to clear this file.


def get_id():
    with open(PORTFOLIO_ID_FILE, "r") as f:
        id = int(f.read())
    with open(PORTFOLIO_ID_FILE, "w") as f:
        f.write(str(id + 1))
    return id


class Portfolio():
    def __init__(self) -> None:
        from global_settings import STARTING_BALANCE, PORTFOLIO_SAVE_DIR
        self.id = get_id()
        self.cash_balance = STARTING_BALANCE
        self.intial_time = current_time()
        self.stock_history = []
        self.portfolio_value = self.cash_balance
        self.path = f"{PORTFOLIO_SAVE_DIR}/{self.id}.json"

    def __dict__(self):
        return {
            "id": self.id,
            "cash_balance": self.cash_balance,
            "initial_time": self.intial_time,
            "stock_history": [t.to_json() for t in self.stock_history],
            "portfolio_value": self.portfolio_value
        }

    def to_json(self):
        return json.dumps(self.__dict__())

    def update_balance(self):
        bal = self.cash_balance
        for t in self.stock_history:
            t = t.__dict__()
            bal += t['total_shares'] * get_stock_price(t['ticker'])
        self.portfolio_value = bal

    def buy_stock(self, ticker: str, amt: int) -> None:
        ticker = ticker.upper()
        price = get_stock_price(ticker)
        if price * amt > self.cash_balance:
            raise ValueError("Insufficient funds")
        self.cash_balance -= price * amt
        if not any(t.ticker == ticker for t in self.stock_history):
            self.stock_history.append(
                UserTickerInteraction(self.id, ticker))
        for t in self.stock_history:
            if t.ticker == ticker:
                ticker = t
                break
        ticker.add_transaction(amt, False, price)
        self.update_balance()

    def get_stock_history(self):
        result = []
        for t in self.stock_history:
            t = t.__dict__()
            result.append(
                f"{t['ticker']}: {t['total_shares']} shares at ${get_stock_price(t['ticker']):.2f} each")
        return "\n".join(result)

    def get_cash_balance(self):
        return float(f"{self.cash_balance:.2f}")

    def save(self):
        with open(self.path, "w") as f:
            f.write(self.to_json())
