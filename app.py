from flask import Flask, render_template, request, redirect, session, jsonify
import json, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "segredo-mesaclick")

SENHA_PAINEL = os.environ.get("SENHA_PAINEL", "1234")
TOTAL_MESAS = 100
DATA_FILE = "data/chamados.json"

# ---------- SETUP ----------
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def init_restaurante(data, restaurante):
    if restaurante not in data:
        data[restaurante] = {}
        for i in range(1, TOTAL_MESAS + 1):
            data[restaurante][str(i)] = False

# ---------- MESA ----------
@app.route("/mesa/<restaurante>/<int:mesa>")
def mesa(restaurante, mesa):
    return render_template("mesa.html", restaurante=restaurante, mesa=mesa)

@app.route("/chamar", methods=["POST"])
def chamar():
    data = load_data()
    restaurante = request.form["restaurante"]
    mesa = str(request.form["mesa"])

    init_restaurante(data, restaurante)
    data[restaurante][mesa] = True
    save_data(data)

    return "
