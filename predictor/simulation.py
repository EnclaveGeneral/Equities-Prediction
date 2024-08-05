import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import io
import base64

def run_simulation(symbol, initial_investment, monthly_contribution, num_months):
    # Download stock data for the last 10 years
    stock = yf.Ticker(symbol)
    data = stock.history(period="10y")

    # Calculate daily returns
    daily_returns = data['Close'].pct_change()

    # Convert index to UTC and remove timezone info
    daily_returns.index = daily_returns.index.tz_convert('UTC').tz_localize(None)

    # Analyze returns
    def analyze_returns(returns, label):
        print(f"\n--- {label} ---")
        print(f"Mean return: {returns.mean():.6f}")
        print(f"Standard deviation: {returns.std():.6f}")

        # Fit to a t-distribution
        t_params = stats.t.fit(returns.dropna())
        df, loc, scale = t_params
        print(f"T-distribution parameters: df={df:.2f}, loc={loc:.6f}, scale={scale:.6f}")

        return df, loc, scale

    # Analyze returns
    params = analyze_returns(daily_returns, f"{symbol} Returns")

    # Monte Carlo Simulation
    np.random.seed(42)

    def simulate_portfolio(num_simulations, num_days):
        results = np.zeros((num_simulations, num_days+1))
        results[:, 0] = initial_investment

        for sim in range(num_simulations):
            portfolio_value = initial_investment

            for day in range(1, num_days+1):
                df, loc, scale = params
                daily_growth = stats.t.rvs(df, loc=loc, scale=scale)
                portfolio_value *= (1 + daily_growth)

                # Add monthly contribution on the first day of each month
                if day % 30 == 1:
                    portfolio_value += monthly_contribution

                results[sim, day] = portfolio_value

        return results

    num_simulations = 2000
    num_days = num_months * 30  # Convert months to days
    results = simulate_portfolio(num_simulations, num_days)

    percentiles = [10, 25, 50, 75, 90]
    percentile_values = np.percentile(results, percentiles, axis=0)

    start_date = pd.Timestamp.now().floor('D')
    dates = [start_date + pd.DateOffset(days=i) for i in range(0, num_days+1, 30)]
    percentile_values_monthly = percentile_values[:, ::30]

    plt.figure(figsize=(12, 6))
    for i, p in enumerate(percentiles):
        plt.plot(dates, percentile_values_monthly[i], label=f'{p}th percentile')

    plt.title(f'{symbol} Portfolio Balance Percentiles Over {num_months} Months')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m/%y'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
    plt.gcf().autofmt_xdate()

    plt.tight_layout()

    # Save plot to BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Prepare final values for each percentile
    final_values = {p: value for p, value in zip(percentiles, percentile_values[:, -1])}

    return graphic, final_values


