class Transaction():
    def __init__(self, amt, time, ticker, sell) -> None:
        self.amount = amt
        self.time = time
        self.ticker = ticker
        self.sell = sell
