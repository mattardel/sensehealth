from flask import Flask, request, url_for, redirect, render_template, jsonify
import json

app = Flask(__name__)

app.config.update(dict(
    dbFile = {},
    pFile = {},
    results = {}
))


@app.route('/', methods=['GET','POST'])
def view_db():
    load_db()
    return render_template("index.html", db_file=app.config['dbFile'], p_file=app.config['pFile'], res=app.config['results'])

def load_db():
    app.config['dbFile'] = dict(read_database())
    app.config['pFile'] = dict(read_persona())
    app.config['results'] = get_results(app.config['pFile'])

def read_database():
    dbList = dict
    with app.open_resource("db.json", mode="r") as f:
        dbList = json.load(f)
    f.close()
    return dbList

def get_metric(db: dict, metric: str):
    try:
        print(db[metric])
    except:
        return metric+" not found."

def read_persona():
    pList = dict
    with app.open_resource("persona.json", mode="r") as f:
        pList = json.load(f)
    f.close()
    return pList

def get_results(db: dict):
    res = dict
    try:
        res = db["results"]
        return res
    except:
        return "Unable to find user results"

# @app.context_processor
# def utility_processor():
#     def get_type(item):
#         return type(item)

@app.route('/user_view', methods=['GET','POST'])
def show_user():
    personaFile=[]
    return render_template("user_view.html", persona_file=personaFile)

if __name__ == '__main__':
    app.run()