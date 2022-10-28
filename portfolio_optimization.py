import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

import yfinance as yf


def main():
    my_green_stocks = [
        # "GOOG",
        # "AAPL",
        # "FB",
        # "BABA",
        # "AMZN",
        "MSFT",
        "LIN",
        "ACN",
        "JBHT",
        "XYL",
        "TXN",
        "CRM",
        "GIL",
        "MCB",
        "INFO",
        "STM",
        "NVDA",
        "ROG",
        "ORCL",
        "MSI",
        "QCOM",
        "SHW",
        "TEL",
        "HPE",
        "EXPO",
    ]

    # Read in price data from yahoo finance
    my_stocks_data = yf.download(my_green_stocks, period="10y")
    my_stocks_data = my_stocks_data.loc[:, "Adj Close"]
    my_stocks_data.index.names = ['date']

    # df = pd.read_csv("stock_prices.csv", parse_dates=True, index_col="date")

    #################################################################################
    #################################################################################
    # OPTIMIZATION
    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(my_stocks_data)
    S = risk_models.sample_cov(my_stocks_data)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.save_weights_to_file("weights.csv")  # saves to file
    print(cleaned_weights)
    ef.portfolio_performance(verbose=True)
    #################################################################################
    #################################################################################

    # Get latest price
    latest_prices = get_latest_prices(my_stocks_data)

    # Calculate how many of each stock can we buy for $100k
    our_budget = 100000
    da = DiscreteAllocation(
        cleaned_weights, latest_prices, total_portfolio_value=our_budget
    )
    allocation, leftover = da.greedy_portfolio()

    # Number of shares per stock
    print("Discrete allocation:", allocation)
    print("Funds remaining: ${:.2f}".format(leftover))


if __name__ == "__main__":
    main()
