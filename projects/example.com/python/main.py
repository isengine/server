from flask import Flask
from os import environ

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>Hello in Python!<h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
