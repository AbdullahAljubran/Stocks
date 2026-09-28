import psycopg2

conn = psycopg2.connect(database="Stocks",
                        user='postgres', password='2664', 
                        host='127.0.0.1', port='5432'
)

conn.autocommit = True
cursor = conn.cursor()

def get_last_datetime():
    sql='''SELECT symbol, MAX(datetime) AS latest
        FROM stock_prices
        WHERE symbol IN ('AMZN', 'AAPL', 'MSFT', 'NVDA', 'TSLA')
        GROUP BY symbol
        ORDER BY symbol;'''
    cursor.execute(sql)
    result=cursor.fetchall()
    for key, value in result:
        print(key,value) 

get_last_datetime()