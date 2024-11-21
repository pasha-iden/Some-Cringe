import psycopg2


a='Классическая художественная литература (русская)'
b='Классическая художественная литература (зарубежная)'
query="SELECT * FROM genres"
datas=[]
try:
    connection = psycopg2.connect(
        host = "127.0.0.1",
        user = "postgres",
        password = "postgres",
        database = "postgres")
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(query)
        # WHERE genre='%s'""" % (a))
        connection.commit()
        d=cursor.fetchall()

except Exception as _ex:
    print ('Error:', _ex)
finally:
    if connection:
        connection.close()

datas=datas+d
print(datas)

# a=[3, 'a', 'b', 'c', 3]
#
# try:
#     connection = psycopg2.connect(
#         host = "127.0.0.1",
#         user = "postgres",
#         password = "postgres",
#         database = "postgres")
#     connection.autocommit = True
#
#     with connection.cursor() as cursor:
#         cursor.execute('''INSERT INTO books (id, bookname, author, genre, numingenre)
#         VALUES ('%s', '%s', '%s', '%s', '%s')''' % (a[0], a[1], a[2], a[3], a[4]))
#         connection.commit()
#
# except Exception as _ex:
#     print ('Error:', _ex)
# finally:
#     if connection:
#         connection.close()

# print (genres)
#
# for i in range(len(genres)):
#     print(genres[i][1])
#
# b=tuple()
# b=b+tuple('a')
# b=b+tuple('b')
# print(b)