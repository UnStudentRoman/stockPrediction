import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta


def linear_trend_forecast(data: pd.DataFrame):
    stock_data = data.copy()

    # Convert Date to numerical values (days since the first date)
    stock_data["Date"] = pd.to_datetime(stock_data["Date"], format="%Y-%m-%d")
    stock_data = stock_data.sort_values("Date")  # Ensure sorted order
    stock_data["Days"] = (stock_data["Date"] - stock_data["Date"].min()).dt.days

    # Prepare data for regression
    X = stock_data["Days"].values.reshape(-1, 1)  # Time as feature
    y = stock_data["Price"].values.reshape(-1, 1)  # Stock prices as target

    # Train Linear Regression model
    model = LinearRegression().fit(X, y)

    # Predict next 3 days
    last_day = stock_data["Days"].max()
    future_days = np.array([last_day + i for i in range(1, 4)]).reshape(-1, 1)
    future_prices = model.predict(future_days)

    # Convert predicted days back to dates
    future_dates = [stock_data["Date"].max() + timedelta(days=i) for i in range(1, 4)]
    future_dates = [item.strftime('%Y-%m-%d') for item in future_dates]

    # Return DataFrame with predictions
    predictions = pd.DataFrame({"Date": future_dates, "Price": future_prices.round(decimals=2).flatten()})

    return predictions


if __name__ == '__main__':
    pass
