import requests
import csv
response = requests.get("https://api.twelvedata.com/time_series?apikey=6224c213ec374d33b749f570c2d8222e&symbol=AAPL&interval=1min&start_date=2026-08-01T21:08:00&end_date=2026-09-27T21:09:00&format=JSON&type=stock")

symbol=response["meta"]["symbol"]
value=response["values"]
rows=[]
for key,value in value.items():
    row=[]
    row.append(symbol)
    row.append(value["datetime"])
    row.append(value["open"])
    row.append(value["high"])
    row.append(value["low"])
    row.append(value["close"])
    row.append(value["volume"])
    rows.append(row)
    
header=["symbol","Date","Opening_value","Highest_Value","Lowest_value","Closing_Value","Volume"]  
with open("Twelve.csv", "w", newline="", encoding="utf-8") as file:
    writer= csv.writer(file)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)