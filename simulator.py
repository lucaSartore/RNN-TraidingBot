from __future__ import annotations
"""
This class is designed to simulate de behavior of the stock market
it uses the data from S&P 500, and pic a date to start the simulation...
"""
from datetime import timedelta
from datetime import date
import pandas as pd


class Simulator:

    DATASET_PATH = r"dataset/filtered/SPY.csv"

    DATASET: pd.DataFrame|None = None

    @classmethod
    def load_dataset(cls) -> None:
        try:
            cls.DATASET = pd.read_csv(cls.DATASET_PATH)
        except FileNotFoundError:
            raise FileNotFoundError("Dataset not found at path: " + cls.DATASET_PATH + " please update the path with the method update_dataset_path")
    
    @classmethod
    def update_dataset_path(cls, new_path: str) -> None:
        cls.DATASET_PATH = new_path
        cls.DATASET = None

    def __init__(self, start_date: date, end_date:date) -> Simulator:
        self.current_date = start_date
        self.end_date = end_date
