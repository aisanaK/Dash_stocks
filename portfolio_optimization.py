import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

import yfinance as yf
from pprint import pprint


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

    print("\nOptimal weights for given stocks:")
    pprint(cleaned_weights)
    print("\n")
    ef.portfolio_performance(verbose=True)
    #################################################################################
    #################################################################################

    # Get latest price
    latest_prices = get_latest_prices(my_stocks_data)
    latest_prices.rename("Latest price", inplace=True)

    # Calculate how many of each stock can we buy for $100k
    our_budget = 100000
    da = DiscreteAllocation(
        cleaned_weights, latest_prices, total_portfolio_value=our_budget
    )
    allocation, leftover = da.greedy_portfolio()

    # Number of shares per stock
    print("\nDiscrete allocation:", allocation)
    print("Funds remaining: ${:.2f}".format(leftover), "\n")

    allocation_df = pd.Series(allocation).to_frame("Quantity")
    allocation_df = allocation_df.join(latest_prices)
    allocation_df["Allocated money"] = allocation_df.prod(axis=1).map('${:,.2f}'.format)

    weights_df = pd.Series(cleaned_weights).to_frame("Weight").query("`Weight` != 0")
    allocation_df = allocation_df.join(weights_df)

    print("Allocation table:\n", allocation_df, "\n")


if __name__ == "__main__":
    main()
