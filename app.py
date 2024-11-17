from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/library')
def index ():
    return render_template("library.html")

if __name__ == "__main__":
    app.run(debug=True)