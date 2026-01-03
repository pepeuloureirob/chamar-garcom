from flask import Flask, render_template, request, redirect, session, jsonify
import json, os, time

app = Flask(__name__)
app.secret_key = "mesaclick-premium"

TOTAL_MESAS = 100

# ----------------- Funções JSON -----------------
def load(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        try:
            return json.load(f)
        except:
            return {}

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ----------------- Arquivos JSON -----------------
DATA_FOLDER = "data"
CHAMADOS = os.path.join(DATA_FOLDER, "chamados.json")
USUARIOS = os.path.join(DATA_FOLDER, "usuarios.json")
CARDAPIOS = os.path.join(DATA_FOLDER, "cardapios.json")

# ----------------- Criação de pastas e arquivos -----------------
os.makedirs(DATA_FOLDER, exist_ok=True)

for f in [CHAMADOS, USUARIOS, CARDAPIOS]:
    if not os.path.exists(f):
        with open(f, "w") as file:
            file.write("{}")

# ----------------- LOGIN -----------------
@app.route("/login/<restaurante>", methods=["GET","POST"])
def login(restaurante):
    erro = False
    usuarios = load(USUARIOS)

    # Cria restaurante com admin padrão se não existir
    if restaurante not in usuarios:
        usuarios[restaurante] = {"admin": {"senha": "admin123", "tipo": "admin"}}
        save(USUARIOS, usuarios)

    if request.method == "POST":
        u = request.form["usuario"].strip()
        s = request.form["senha"].strip()
        if u in usuarios[restaurante] and usuarios[restaurante][u]["senha"] == s:
            session["user"] = u
            session["tipo"] = usuarios[restaurante][u]["tipo"]
            session["restaurante"] = restaurante
            return redirect(f"/painel/{restaurante}")
        erro = True

    return render_template("login.html", erro=erro, restaurante=restaurante)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ----------------- MESA -----------------
@app.route("/mesa/<restaurante>/<int:mesa>")
def mesa(restaurante, mesa):
    cardapios = load(CARDAPIOS)
    link = cardapios.get(restaurante, "")
    return render_template("mesa.html", restaurante=restaurante, mesa=mesa, cardapio=link)

@app.route("/chamar", methods=["POST"])
def chamar():
    data = load(CHAMADOS)
    r = request.form["restaurante"]
    m = str(request.form["mesa"])
    data.setdefault(r, {})
    data[r][m] = time.time()
    save(CHAMADOS, data)
    return "ok"

# ----------------- PAINEL --
