from manage_times import current_time, time_for_json
from global_settings import PORTFOLIO_ID_PATH
import json
from stock_data import get_stock_price
from user_ticker_interactions import UserTickerInteraction


def get_id():
    with open(PORTFOLIO_ID_PATH, "r") as f:
        id = int(f.read())
    with open(PORTFOLIO_ID_PATH, "w") as f:
        f.write(str(id + 1))
    return id


class Portfolio():
    def __init__(self) -> None:
        from global_settings import STARTING_BALANCE, PORTFOLIO_JSON_SAVE_DIR, PORTFOLIO_PICKLE_SAVE_DIR
        self.id = get_id()
        self.cash_balance = STARTING_BALANCE
        self.intial_time = current_time()
        self.stock_history = []
        self.portfolio_value = self.cash_balance
        self.path = f"{PORTFOLIO_JSON_SAVE_DIR}/{self.id}.json"
        self.pickle_path = f"{PORTFOLIO_PICKLE_SAVE_DIR}/{self.id}.pkl"
        # self.save() # TODO

    def __dict__(self):
        return {
            "id": self.id,
            "cash_balance": self.cash_balance,
            "initial_time": time_for_json(self.intial_time),
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

    def save_as_json(self):
        with open(self.path, "w") as f:
            json.dump(self.__dict__(), f, indent=4)

    def load_from_pickle(self):
        pass

    def save_as_pickle(self):
        pass


def save_as_pickle(obj):
    import pickle
    with open(obj.pickle_path, 'wb') as file:
        pickle.dump(obj, file)


def load_from_pickle(id):
    import pickle
    from global_settings import PORTFOLIO_PICKLE_SAVE_DIR
    with open(f"{PORTFOLIO_PICKLE_SAVE_DIR}/{id}.pkl", 'rb') as file:
        return pickle.load(file)


max = Portfolio()
max.buy_stock("AAPL", 5)
save_as_pickle(max)
max = load_from_pickle(max.id)
print(max.cash_balance)
print(max.get_stock_history())
# TODO a way of loading from file.
# TODO fix the format of the JSONs that are written, they are weird and full of break chars
