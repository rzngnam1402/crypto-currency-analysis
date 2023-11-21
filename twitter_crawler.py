import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import re


def scrape_bitcoin_tweet_volume():
    url = 'https://bitinfocharts.com/comparison/bitcoin-tweets.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the script tag containing the data
    script = soup.find(
        'script', text=lambda t: t and 'new Dygraph(document.getElementById("container")' in t)
    if not script:
        return "Data not found in the page"

    # Extracting and cleaning the data string
    data_str = script.string.split(
        'new Dygraph(document.getElementById("container")')[1]
    data_str = data_str.split(']);')[0].split('[[')[1]

    # Parsing the data
    data = []
    for row in data_str.split('],['):
        # Using regular expression to extract date and tweet count
        match = re.match(r"new Date\((\d{4}/\d{2}/\d{2})\),(\d+)", row)
        if match:
            date_str, tweet_count = match.groups()
            date = datetime.strptime(date_str, '%Y/%m/%d')
            tweet_count = int(tweet_count)
            data.append((date, tweet_count))

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Tweet Count'])

    # Optionally filter data for the latest month or any specific time range
    last_month = datetime.now() - timedelta(days=30)
    df = df[df['Date'] > last_month]

    return df


# Call the function and print the result
tweet_volume_data = scrape_bitcoin_tweet_volume()
print(tweet_volume_data)
