from flask import Flask, request, url_for, redirect, render_template, jsonify
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    print(read_database())
    return "Hello World!"


def read_database():
    f_string = ""
    with open("database.txt","r") as f:
        f_string = f.read()
        print(f_string)
    f.close()
    return f_string

if __name__ == '__main__':
    app.run()
