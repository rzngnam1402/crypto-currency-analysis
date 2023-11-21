import requests
import pandas as pd


def fetch_bitcoin_data(days_to_fetch, months_to_fetch):
    url = (
        f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        f"?vs_currency=usd&interval=daily&days={days_to_fetch}"
    )

    response = requests.get(url)
    data = response.json()

    # Extracting price data
    prices = data['prices']

    df = pd.DataFrame(prices, columns=['timestamp', 'price'])

    # Convert timestamp to date
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date

    df['date'] = pd.to_datetime(df['date'])

    # Set 'date' as the index
    df.set_index('date', inplace=True)

    # Drop the now redundant 'timestamp' column
    df.drop('timestamp', axis=1, inplace=True)

    # Resample to get daily high, low, open, and close
    daily_df = df['price'].resample('D').ohlc()

    return daily_df


if __name__ == '__main__':
    days_to_fetch = 365*2
    months_to_fetch = days_to_fetch // 30
    bitcoin_data = fetch_bitcoin_data(days_to_fetch, months_to_fetch)
    bitcoin_data.to_csv('./data/bitcoin_prices.csv', index=False)

    print("Bitcoin data for the last " + str(months_to_fetch) +
          " months has been saved to ./data/bitcoin_prices.csv")
