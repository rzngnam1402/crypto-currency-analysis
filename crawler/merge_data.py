import requests
import pandas as pd


def merge_data(data_path_1, data_path_2):
    btc_ohlc = pd.read_csv(data_path_1)
    btc_twitter_volume = pd.read_csv(data_path_2)

    # Merge the files on the timestamp column
    merged_data = pd.merge(btc_ohlc, btc_twitter_volume,
                           on='timestamp', how='left')

    merged_data.head()
    merged_data.to_csv('../data/BTC_Merged.csv')


if __name__ == '__main__':
    merge_data('../data/BTC_OHLC.csv', '../data/BTC_TwitterVolume.csv')
