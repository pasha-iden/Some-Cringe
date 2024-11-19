import psycopg2
from flask import Flask, render_template, url_for

app = Flask(__name__)

def bookslist():
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
            books=cursor.fetchall()
    except Exception as _ex:
        print ('Error:', _ex)
    finally:
        if connection:
            connection.close()
    return books

@app.route('/library')
def index ():
    books = bookslist()
    return render_template("library.html", bookslistprint=books)

if __name__ == "__main__":
    app.run(debug=True)