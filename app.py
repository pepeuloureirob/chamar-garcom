from flask import Flask, render_template, request, redirect, session, jsonify
import json, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-padrao")

# SENHA DO PAINEL (vem do Render)
SENHA_PAINEL = os.environ.get("SENHA_PAINEL", "1234")

DATA_FILE = "data/chamados.json"
TOTAL_MESAS = 100

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
        for m in range(1, TOTAL_MESAS + 1):
            data[restaurante][str(m)] = False

# ---------- MESA (CELULAR) ----------
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
    return "ok"

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = False
    if request.method == "POST":
        if request.form["senha"] == SENHA_PAINEL:
            session["logado"] = True
            return redirect("/painel")
        else:
            erro = True
    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------- PAINEL ----------
@app.route("/painel")
def painel():
    if not session.get("logado"):
        return redirect("/login")
    return render_template("painel.html")

@app.route("/status")
def status():
    if not session.get("logado"):
        return jsonify({})
    return jsonify(load_data())

@app.route("/atender", methods=["POST"])
def atender():
    if not session.get("logado"):
        return "não autorizado", 403

    data = load_data()
    restaurante = request.form["restaurante"]
    mesa = str(request.form["mesa"])

    init_restaurante(data, restaurante)
    data[restaurante][mesa] = False
    save_data(data)
    return "ok"
