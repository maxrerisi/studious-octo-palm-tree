from manage_times import current_time
from global_settings import PORTFOLIO_ID_FILE
import json


def get_id():
    with open(PORTFOLIO_ID_FILE, "r") as f:
        id = int(f.read())
    with open(PORTFOLIO_ID_FILE, "w") as f:
        f.write(str(id + 1))
    return id


class Portfolio():
    def __init__(self) -> None:
        from global_settings import STARTING_BALANCE
        self.id = get_id()
        self.balance = STARTING_BALANCE
        self.intial_time = current_time()
        self.transactions = []
        self.START_BAL = STARTING_BALANCE

    def __dict__(self):
        return {
            "id": self.id,
            "balance": self.balance,
            "initial_time": self.intial_time,
            "transactions": [t.__dict__() for t in self.transactions]
        }

    def to_json(self):
        return json.dumps(self.__dict__())

    def update_balance(self):
        bal = self.START_BAL
        for t in self.transactions:
            t = t.__dict__()
            if t['buy']:
                # TODO this is the next place to fix
                self.balance += t['total']
