from __future__ import annotations
"""
This class is designed to simulate de behavior of the stock market
it uses the data from S&P 500, and pic a date to start the simulation...
Note: the simulation dose not take into account the dividends
"""
from datetime import timedelta
from datetime import date
import pandas as pd

# difference between the buy and sell price
SPREAD = 0.005 # % over the price


class Simulator:

    DATASET_PATH = r"dataset/raw/SPY.csv"
    DATASET: pd.DataFrame|None = None
    MIN_DATE: date|None = None
    MAX_DATE: date|None = None


    @classmethod
    def load_dataset(cls) -> None:
        try:
            cls.DATASET = pd.read_csv(cls.DATASET_PATH)
            cls.DATASET["Date"] = cls.DATASET["Date"].apply(lambda x: date.fromisoformat(x))
            cls.MAX_DATE = cls.DATASET["Date"].max()
            cls.MIN_DATE = cls.DATASET["Date"].min()
        except FileNotFoundError:
            raise FileNotFoundError("Dataset not found at path: " + cls.DATASET_PATH + " please update the path with the method update_dataset_path")
    
    @classmethod
    def update_dataset_path(cls, new_path: str) -> None:
        cls.DATASET_PATH = new_path
        cls.DATASET = None
        Simulator.load_dataset()
        

    def __init__(self, start_date: date, end_date:date, start_cash: float = 1000) -> Simulator:
        if self.DATASET is None:
            Simulator.load_dataset()
        if start_date < self.MIN_DATE:
            raise ValueError("Start date is before the dataset, please choose a date after: " + str(self.MIN_DATE))
        if end_date > self.MAX_DATE:
            raise ValueError("End date is after the dataset, please choose a date before: " + str(self.MAX_DATE))
        self.total_invested_cash: float = start_cash
        self.stock_owned: float = 0.0
        self.cash_available: float = start_cash
        self.current_date: date = start_date
        self.end_date: date = end_date
        # make sure the market is open when the simulation start
        self.next_open_day()

    def get_current_price(self) -> float:
        return self.DATASET[self.DATASET["Date"] == self.current_date]["Close"].iloc[0]

    def insert_funds(self, amount: float) -> None:
        self.total_invested_cash += amount
        self.cash_available += amount

    def buy(self) -> None:
        self.stock_owned += self.cash_available / (self.get_current_price()*(1+SPREAD))
        self.cash_available = 0.0

    def sell(self) -> None:
        self.cash_available += self.stock_owned * self.get_current_price()*(1-SPREAD)
        self.stock_owned = 0.0

    def get_current_value(self) -> float:
        return self.stock_owned * self.get_current_price() + self.cash_available
    
    def get_current_roi(self) -> float:
        return round(((self.get_current_value()) / self.total_invested_cash - 1.0)*100.0,2)
    

    def next_open_day(self) -> None:
        while not self.is_market_open():
            self.next_day()

    def next_day(self) -> None:
        self.current_date += timedelta(days=1)
        if self.current_date > self.end_date:
            raise StopIteration("End of simulation")
        self.next_open_day()
        
    def is_market_open(self) -> bool:
        return not self.DATASET[self.DATASET["Date"] == self.current_date].empty
        

def test_1():    
    sim = Simulator(date(2009, 1, 1), date(2019, 1, 10))
    sim.buy()
    roi = sim.get_current_roi()
    print("roi: ", roi)


    # wait 2 years
    for _ in range(365*6):
        sim.next_day()
    
    print("current date: ", sim.current_date)

    roi = sim.get_current_roi()
    print(f"roi after years: {roi}%")
    



if __name__ == "__main__":
    test_1()