import requests
import json
import pandas
import csv
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=T4CAGB0ODKJ7YNMT'
r = requests.get(url)
data = r.json()

symbol=data["Meta Data"]["2. Symbol"]
Monthly_Time_Series=data["Monthly Time Series"]
rows=[]
for key,value in Monthly_Time_Series.items():
    row=[]
    row.append(key)
    row.append(symbol)
    row.append(value["1. open"])
    row.append(value["2. high"])
    row.append(value["3. low"])
    row.append(value["4. close"])
    row.append(value["5. volume"])
    rows.append(row)
    

header=["Date","Stock_Symbol","Opening_value","Highest_Value","Lowest_value","Closing_Value","Volume"]  
with open("Output.csv", "w", newline="", encoding="utf-8") as file:
    writer= csv.writer(file)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)

