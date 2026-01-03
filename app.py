from flask import Flask, render_template, request, redirect, session, jsonify
import json, os, time

app = Flask(__name__)
app.secret_key = "mesaclick-premium"

TOTAL_MESAS = 100

# ----------------- Funções de leitura/escrita JSON -----------------
def load(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ----------------- Arquivos JSON -----------------
CHAMADOS = "data/chamados.json"
USUARIOS = "data/usuarios.json"
CARDAPIOS = "data/cardapios.json"

# ----------------- Criação de pastas -----------------
for p in ["data"]:
    os.makedirs(p, exist_ok=True)

# ----------------- LOGIN -----------------
@app.route("/login/<restaurante>", methods=["GET","POST"])
def login(restaurante):
    erro = False
    usuarios = load(USUARIOS)
    
    # Cria restaurante com admin padrão se não existir
    if restaurante not in usuarios:
        usuarios[restaurante] = {
            "admin": {"senha": "admin123", "tipo": "admin"}
        }
        save(USUARIOS, usuarios)

    if request.method == "POST":
        u = request.form["usuario"]
        s = request.form["senha"]

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
    m = request.form["mesa"]

    data.setdefault(r, {})
    data[r][m] = time.time()
    save(CHAMADOS, data)
    return "ok"

# ----------------- PAINEL -----------------
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

# ----------------- ADMIN -----------------
@app.route("/usuarios/<restaurante>", methods=["GET","POST"])
def usuarios(restaurante):
    if session.get("tipo") != "admin":
        return "acesso negado", 403

    usuarios_data = load(USUARIOS)
    usuarios_data.setdefault(restaurante, {})

    if request.method == "POST":
        usuarios_data[restaurante][request.form["usuario"]] = {
            "senha": request.form["senha"],
            "tipo": request.form["tipo"]
        }
        save(USUARIOS, usuarios_data)

    return render_template("usuarios.html", usuarios=usuarios_data[restaurante])

@app.route("/cardapio/<restaurante>", methods=["POST"])
def cardapio(restaurante):
    if session.get("tipo") != "admin":
        return "negado", 403

    cardapios = load(CARDAPIOS)
    cardapios[restaurante] = request.form["link"]
    save(CARDAPIOS, cardapios)
    return redirect(f"/painel/{restaurante}")

# ----------------- ROTA PRINCIPAL -----------------
@app.route("/")
def index():
    return "Sistema MesaClick Premium – Acesse /login/<restaurante>"

# ----------------- EXECUÇÃO -----------------
if __name__ == "__main__":
    app.run()

