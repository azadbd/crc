from flask import Flask, render_template, request, session
from flask_session import Session
import requests
import datetime

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
res = requests.get("http://data.fixer.io/api/latest", params={"access_key":"83bfbfdd2206026ccd7612f300662814"})

if res.status_code != 200:
    raise Exception("Error: Something went wrong!")

data = res.json()
unixdt = data["timestamp"]
tstamp = datetime.datetime.fromtimestamp(int(unixdt)).strftime('%Y-%m-%d %H:%M:%S')
@app.route("/")
def index():
    headline = "Foreign exchange rates and currency conversion"
    return render_template("index.html", headlines=headline, data = data)

@app.route("/", methods=['POST'])
def convert_currency():
    headline = "Currency Rate Conversion"
    userdbase   = request.form.get("defaultbase")
    userabase   = request.form.get("askingbase")
    userdbaser  = float(data["rates"][userdbase])
    userabaser  = float(data["rates"][userabase])
    session["baserate"]     = userdbaser
    session["basecurrency"] = userdbase

    if userdbaser >= 1:
        rate = round(userabaser/userdbaser,6)
    else:
        rate = round(userabaser*userdbaser,12)

    conversion = f"1 {userdbase} = {rate} {userabase}"
    return render_template("index.html", headlines=headline, conversion = conversion, data = data)


@app.route("/all_currency")
def all_currency():
    return render_template("allcurrency.html", data = data, basecurrency = session["basecurrency"], baserate = session["baserate"],tstamp=tstamp )
