import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="botpress",
    user="postgres",
    password="milanforever"
)
cursor = conn.cursor()
query = 'select * from strategy_default'
cursor.execute(query)
print(cursor.fetchall())