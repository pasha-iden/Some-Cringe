import psycopg2


try:
    connection = psycopg2.connect(
        host = "127.0.0.1",
        user = "postgres",
        password = "postgres",
        database = "postgres")
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM books''')
        connection.commit()
        genres=cursor.fetchall()

except Exception as _ex:
    print ('Error:', _ex)
finally:
    if connection:
        connection.close()

print (genres)

for i in range(len(genres)):
    print(genres[i][1])