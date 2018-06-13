from flask import Flask, request, url_for, redirect, render_template, jsonify
import json

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def hello_world():
    dbFile = read_database()
    return render_template("index.html", db_file=dbFile)


def read_database():
    dbList = []
    with app.open_resource("db.json", mode="r") as f:
        dbList = json.load(f)
    f.close()
    return dbList

@app.route('/user_view', methods=['GET','POST'])
def show_user():
    personaFile=[]
    return render_template("user_view.html", persona_file=personaFile)

if __name__ == '__main__':
    app.run()
