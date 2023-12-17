# I want to remove some information from the original data that could point the neural network to the specific year...
# To avoid overfitting
# To do so i will remove the year as an information, and keep only the month and day
# also the value of the index could int to the year, so instead of the absolute value i will keep the 
# gain or loss over the previous day
import pandas as pd
import numpy as np
import datetime as dt

def main():
    input_file = "dataset/raw/SPY.csv"

    input_df = pd.read_csv(input_file, index_col=0)

    input_df.reset_index(inplace=True)

    input_df["Date"] = input_df["Date"].apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d").date())

    input_df["Month"] = input_df["Date"].apply(lambda x: x.month)
    input_df["Day"] = input_df["Date"].apply(lambda x: x.day)

    # express open, high, low, close as a percentage of the previous day
    for col in ["Open", "High", "Low", "Close","Adj Close", "Volume"]:
        input_df[col] = input_df[col] / input_df[col].shift(1)
        input_df[col] = input_df[col].apply(lambda x: x - 1.0)
        input_df[col].iloc[0] = 0.0

    input_df.drop(["Date"], axis=1, inplace=True)

    input_df.to_csv("dataset/filtered/SPY.csv")


if __name__ == "__main__":
    main()