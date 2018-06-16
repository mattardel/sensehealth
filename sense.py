from flask import Flask, request, url_for, redirect, render_template, jsonify
import json

app = Flask(__name__)

app.config.update(dict(
    dbFile = {},
    pFile = {},
    results = {}
))


@app.route('/', methods=['GET','POST'])
def open_home():
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

def get_metric_from_db(db: dict, metric: str):
    try:
        return(db[metric])
    except:
        return None

def get_metric_from_persona(persona: dict, metric: str):
    try:
        return(persona['result_num'][metric])
    except:
        return None

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

@app.route('/about')
def open_about():
    return render_template("about.html")

@app.route('/health_metrics', methods=['GET','POST'])
def get_metrics():
    load_db()
    dbList = list(app.config['dbFile'].keys())
    mid = len(dbList)//2
    db1 = dbList[0:mid]
    db2 = dbList[mid:]
    return render_template("health_metrics.html", db1=db1, db2=db2)

@app.route('/metric_exp/')
@app.route('/metric_exp/<metric>')
def explain_metric(metric=None):
    db = app.config['dbFile']
    persona = app.config['pFile']
    page_info = []

    if metric != None:
        met_info = get_metric_from_db(db, metric)
        met_num = get_metric_from_persona(persona, metric)
        if(met_info != None):
            page_info.append(persona['results'][metric])
            page_info.append(met_info['description'])
            range = [met_info['low_number'], met_info['high_number']]
            print(range)
            print(met_num)
            if(met_num < range[0]):
                page_info.append('LOW')
                page_info.append(met_info['low'])
            elif(met_num > range[1]):
                page_info.append('HIGH')
                page_info.append(met_info['high'])
            else:
                page_info.append('NORMAL')
                page_info.append(met_info['normal'])

    return render_template('metric_exp.html', metric=metric, page_info=page_info)

if __name__ == '__main__':
    app.run()
