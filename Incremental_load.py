import psycopg2
import requests
import datetime
from config import API_KEY
from config import PostgreSQL_Password
conn = psycopg2.connect(database="Stocks",
                        user='postgres', password=PostgreSQL_Password, 
                        host='127.0.0.1', port='5432'
)

conn.autocommit = False
cursor = conn.cursor()

All_data=[]
dic={}
failed_symbols = []
def get_last_datetime():
    sql='''SELECT symbol, MAX(datetime) AS latest
        FROM stock_prices
        WHERE symbol IN ('AMZN', 'AAPL', 'MSFT', 'NVDA', 'TSLA')
        GROUP BY symbol
        ORDER BY symbol;'''
    cursor.execute(sql)
    result=cursor.fetchall()
    
    for key, value in result:
        start_date=value.strftime("%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dic[key]=start_date
        response = requests.get(
            "https://api.twelvedata.com/time_series",
            params={
                "apikey": API_KEY,
                "symbol": key,
                "interval": "1h",
                "start_date": start_date,
                "end_date" : end_date,
            },
            timeout=30
        )

        data = response.json()

        if response.status_code != 200:
            print("HTTP error:", key, response.status_code)
            failed_symbols.append(key)
            continue

        if data.get("status") == "error" or "values" not in data:
            print("API error:", key, data.get("message", data))
            continue

        All_data.append(data)



get_last_datetime()
new_list=[]
for data in All_data:
    for row in data["values"]:
        if row["datetime"] > dic[data["meta"]["symbol"]]:
            new_list.append((data["meta"]["symbol"],row))
        else:
            pass


sql = """
    INSERT INTO stock_prices
    (symbol, datetime, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for symbol, row in new_list:
    values = (
        symbol,
        row["datetime"],
        row["open"],
        row["high"],
        row["low"],
        row["close"],
        row["volume"]
    )
    cursor.execute(sql, values)
conn.commit()

print("New records:", len(new_list))
print("Failed symbols:", failed_symbols)
print("Successfully fetched(number of symbols):", len(All_data))
print("New records:", len(new_list))
