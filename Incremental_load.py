import psycopg2
import requests
from config import API_KEY
conn = psycopg2.connect(database="Stocks",
                        user='postgres', password='2664', 
                        host='127.0.0.1', port='5432'
)

conn.autocommit = True
cursor = conn.cursor()

All_data=[]
dic={}
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
        
        dic[key]=start_date
        response = requests.get(
                "https://api.twelvedata.com/time_series",
                params={
                    "apikey": API_KEY,
                    "symbol": key,
                    "interval": "1h",
                    "start_date": start_date,
                    "end_date": "2026-09-28T20:37:00",
                }
        )
        data = response.json()
        All_data.append(data)    


print(get_last_datetime())

for data in All_data:
    for row in data["values"]:
        if row["datetime"] > dic[data["meta"]["symbol"]]:
            print(row["datetime"])
        else:
            pass
        
        
