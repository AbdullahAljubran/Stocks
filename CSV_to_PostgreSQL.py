import psycopg2

conn = psycopg2.connect(database="Stocks",
                        user='postgres', password='2664', 
                        host='127.0.0.1', port='5432'
)

conn.autocommit = True
cursor = conn.cursor()


def table_creation():
    sql = '''Create Table stock_prices(
    date DATE, 
    "symbol" VARCHAR(10),
    "open" DECIMAL(12,4),
    "high" DECIMAL(12,4),
    "low" DECIMAL(12,4),
    "close" DECIMAL(12,4),
    "volume" BIGINT,
    PRIMARY KEY (symbol, date)
    );'''

    cursor.execute(sql)

def table_load():
    file_path= '/Users/abdullahaljubran/Documents/Projects/Data Engineer Projects/Stocks Project/Output.csv'
    with open(file_path, "r") as file:
        cursor.copy_expert(
            """
            COPY stock_prices(date, symbol, open, high, low, close, volume)
            FROM STDIN
            WITH CSV HEADER
            """,
            file
        )
    

def table_select():
    sql3 = '''select * from stock_prices;'''
    cursor.execute(sql3)
    for i in cursor.fetchall():
        print(i)
    print("Load is done")

table_creation()
table_load()
table_select()
conn.commit()
conn.close()