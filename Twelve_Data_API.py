import requests
import csv

stocks=["AAPL","MSFT","NVDA","TSLA","AMZN"]

all_data = []

for stock in stocks:

    response = requests.get(
        "https://api.twelvedata.com/time_series",
        params={
            "apikey": "6224c213ec374d33b749f570c2d8222e",
            "symbol": stock,
            "interval": "1h",
            "start_date": "2026-09-01T20:37:00",
            "end_date": "2026-09-28T20:37:00",
        }
    )

    data = response.json()

    all_data.append(data)

with open("stock_prices.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    # Header
    writer.writerow([
        "symbol",
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ])

    # Data
    for data in all_data:

        symbol = data["meta"]["symbol"]

        for value in data["values"]:

            writer.writerow([
                symbol,
                value["datetime"],
                value["open"],
                value["high"],
                value["low"],
                value["close"],
                value["volume"]
            ])

print("CSV created successfully!")