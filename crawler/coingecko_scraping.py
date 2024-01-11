import requests
import pandas as pd


def clean_data():
    data = pd.read_csv('../data/BTC.csv')
    print(data.tail(5))
    data.drop('ticker', axis=1, inplace=True)
    print(data.tail(5))
    data.to_csv('../data/BTC.csv', index=False)


def fetch_bitcoin_data():
    url = (
        f"https://api.coingecko.com/api/v3/coins/bitcoin/ohlc"
        f"?vs_currency=usd&days=7&precision=1"
    )

    response = requests.get(url)
    data = response.json()

    columns = ['timestamp', 'open', 'high', 'low', 'close']
    coin_ohlc = pd.DataFrame(data, columns=columns)

    coin_ohlc['timestamp'] = pd.to_datetime(coin_ohlc['timestamp'], unit='ms')
    coin_ohlc.set_index('timestamp', inplace=True)
    daily_ohlc = coin_ohlc.resample('1D').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    })

    # remove the first and last daily ohlc to increase accuracy
    daily_ohlc = daily_ohlc.iloc[1:-1]
    print(daily_ohlc)

    existing_data = pd.read_csv('../data/BTC_OHLC.csv')
    existing_data.rename(columns={'date': 'timestamp'}, inplace=True)
    existing_data.set_index('timestamp', inplace=True)
    print(existing_data.tail(5))

    existing_data.update(daily_ohlc)
    print(existing_data.tail(5))

    existing_data.to_csv('../data/BTC_OHLC.csv')


if __name__ == '__main__':
    bitcoin_data = fetch_bitcoin_data()
    # bitcoin_data.to_csv('../data/bitcoin_prices.csv', index=False)
