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
        u = request.form["usuario"].strip()
        s = request.form["senha"].strip()

        if u in usuarios[restaurante] and usu

