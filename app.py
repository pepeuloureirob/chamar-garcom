from flask import Flask, render_template, request, redirect, session, jsonify
import json, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mesaclick-seguro")

SENHA_PAINEL = os.environ.get("SENHA_PAINEL", "1234")
TOTAL_MESAS = 100
DATA_FILE = "data/chamados.json"

# ---------- SETUP ----------
os.makedirs("data", exist_ok=True)

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
        data[restaurante] = {
            "mesas": {str(i): False for i in range(1, TOTAL_MESAS + 1)},
            "cardapio": ""
        }

# ---------- MESA ----------
@app.route("/mesa/<restaurante>/<int:mesa>")
def mesa(restaurante, mesa):
    data = load_data()
    init_restaurante(data, restaurante)
    cardapio = data[restaurante]["cardapio"]
    return render_template("mesa.html", restaurante=restaurante, mesa=mesa, cardapio=cardapio)

@app.route("/chamar", methods=["POST"])
def chamar():
    data = load_data()
    restaurante = request.form["restaurante"]
    mesa = request.form["mesa"]

    init_restaurante(data, restaurante)
    data[restaurante]["mesas"][mesa] = True
    save_data(data)
    return "ok"

# ---------- LOGIN ----------
@app.route("/login/<restaurante>", methods=["GET", "POST"])
def login(restaurante):
    erro = False
    if request.method == "POST":
        if request.form["senha"] == SENHA_PAINEL:
            session["logado"] = True
            session["restaurante"] = restaurante
            return redirect(f"/painel/{restaurante}")
        erro = True
    return render_template("login.html", restaurante=restaurante, erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- PAINEL ----------
@app.route("/painel/<restaurante>")
def painel(restaurante):
    if not session.get("logado") or session.get("restaurante") != restaurante:
        return redirect(f"/login/{restaurante}")
    return render_template("painel.html", restaurante=restaurante, total=TOTAL_MESAS)

@app.route("/status/<restaurante>")
def status(restaurante):
    if not session.get("logado"):
        return jsonify({"erro": "não autorizado"}), 403
    data = load_data()
    init_restaurante(data, restaurante)
    return jsonify(data[restaurante])

@app.route("/atender", methods=["POST"])
def atender():
    data = load_data()
    restaurante = request.form["restaurante"]
    mesa = request.form["mesa"]

    init_restaurante(data, restaurante)
    data[restaurante]["mesas"][mesa] = False
    save_data(data)
    return "ok"

@app.route("/cardapio", methods=["POST"])
def cardapio():
    data = load_data()
    restaurante = request.form["restaurante"]
    link = request.form["link"]

    init_restaurante(data, restaurante)
    data[restaurante]["cardapio"] = link
    save_data(data)
    return redirect(f"/painel/{restaurante}")

if __name__ == "__main__":
    app.run()
