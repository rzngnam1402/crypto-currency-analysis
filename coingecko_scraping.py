import requests
import pandas as pd


def fetch_bitcoin_data():
    url = (
        f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        f"?vs_currency=usd&interval=daily&days=max"
    )

    response = requests.get(url)
    data = response.json()

    prices = data['prices']  # List of [timestamp, price]
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    # Resampling to daily OHLC data
    ohlc_df = df['price'].resample('1D').ohlc()
    ohlc_df.reset_index(inplace=True)

    return ohlc_df


if __name__ == '__main__':
    bitcoin_data = fetch_bitcoin_data()
    bitcoin_data.to_csv('./data/bitcoin_prices.csv', index=False)
