from flask import Flask, render_template, request, redirect, session, jsonify
import json, os, time

app = Flask(__name__)
app.secret_key = "mesaclick-premium"

TOTAL_MESAS = 100

def load(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

CHAMADOS = "data/chamados.json"
USUARIOS = "data/usuarios.json"
CARDAPIOS = "data/cardapios.json"

for p in ["data"]:
    os.makedirs(p, exist_ok=True)

# ---------- LOGIN ----------
@app.route("/login/<restaurante>", methods=["GET","POST"])
def login(restaurante):
    erro = False
    if request.method == "POST":
        usuarios = load(USUARIOS)
        u = request.form["usuario"]
        s = request.form["senha"]

        if restaurante in usuarios and u in usuarios[restaurante]:
            if usuarios[restaurante][u]["senha"] == s:
                session["user"] = u
                session["tipo"] = usuarios[restaurante][u]["tipo"]
                session["restaurante"] = restaurante
                return redirect(f"/painel/{restaurante}")
        erro = True

    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- MESA ----------
@app.route("/mesa/<restaurante>/<int:mesa>")
def mesa(restaurante, mesa):
    cardapios = load(CARDAPIOS)
    link = cardapios.get(restaurante, "")
    return render_template("mesa.html", restaurante=restaurante, mesa=mesa, cardapio=link)

@app.route("/chamar", methods=["POST"])
def chamar():
    data = load(CHAMADOS)
    r = request.form["restaurante"]
    m = request.form["mesa"]

    data.setdefault(r, {})
    data[r][m] = time.time()
    save(CHAMADOS, data)
    return "ok"

# ---------- PAINEL ----------
@app.route("/painel/<restaurante>")
def painel(restaurante):
    if "user" not in session:
        return redirect(f"/login/{restaurante}")
    return render_template("painel.html", restaurante=restaurante)

@app.route("/status/<restaurante>")
def status(restaurante):
    data = load(CHAMADOS)
    return jsonify(data.get(restaurante, {}))

@app.route("/atender", methods=["POST"])
def atender():
    data = load(CHAMADOS)
    r = request.form["restaurante"]
    m = request.form["mesa"]
    data.get(r, {}).pop(m, None)
    save(CHAMADOS, data)
    return "ok"

# ---------- ADMIN ----------
@app.route("/usuarios/<restaurante>", methods=["GET","POST"])
def usuarios(restaurante):
    if session.get("tipo") != "admin":
        return "acesso negado", 403

    usuarios = load(USUARIOS)
    usuarios.setdefault(restaurante, {})

    if request.method == "POST":
        usuarios[restaurante][request.form["usuario"]] = {
            "senha": request.form["senha"],
            "tipo": request.form["tipo"]
        }
        save(USUARIOS, usuarios)

    return render_template("usuarios.html", usuarios=usuarios[restaurante])

@app.route("/cardapio/<restaurante>", methods=["POST"])
def cardapio(restaurante):
    if session.get("tipo") != "admin":
        return "negado", 403

    cardapios = load(CARDAPIOS)
    cardapios[restaurante] = request.form["link"]
    save(CARDAPIOS, cardapios)
    return redirect(f"/painel/{restaurante}")

if __name__ == "__main__":
    app.run()
