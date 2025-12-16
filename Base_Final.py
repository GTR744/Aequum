import os, json, time, hashlib
from threading import Thread
from flask import Flask, request, jsonify, render_template_string
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
from waitress import serve

# ==============================
# CONFIGURATION
# ==============================
BLOCK_TIME = 30  # secondes par cycle
SAVE_CYCLES = 10

CHILD_MONTHLY = 750
ADO_MONTHLY = 1000
ADULT_MONTHLY = 1500

CHILD_USABLE = 0.5
ADO_USABLE = 0.6
ADULT_USABLE = 0.8

DATA_CHAIN = "blockchain.json"
DATA_WALLETS = "wallets.json"
BACKUP_DIR = "backups"

# ==============================
# INIT
# ==============================
app = Flask(__name__)
chain = []
wallets = {}
mempool = []
nonces = {}

os.makedirs(BACKUP_DIR, exist_ok=True)

# ==============================
# UTILITAIRES
# ==============================
def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def save_state():
    json.dump(chain, open(DATA_CHAIN, "w"), indent=2)
    json.dump(wallets, open(DATA_WALLETS, "w"), indent=2)

    if chain:
        idx = chain[-1]["index"]
        backup_file = f"{BACKUP_DIR}/backup_{idx}.json"
        json.dump({"chain": chain, "wallets": wallets}, open(backup_file, "w"), indent=2)

        files = sorted(os.listdir(BACKUP_DIR))
        while len(files) > SAVE_CYCLES:
            os.remove(os.path.join(BACKUP_DIR, files.pop(0)))

def load_state():
    global chain, wallets
    if os.path.exists(DATA_CHAIN):
        chain = json.load(open(DATA_CHAIN))
    if os.path.exists(DATA_WALLETS):
        wallets = json.load(open(DATA_WALLETS))

# ==============================
# BLOCKCHAIN
# ==============================
def genesis():
    if not chain:
        chain.append({
            "index": 0,
            "timestamp": time.time(),
            "transactions": [],
            "prev_hash": "0",
            "hash": "GENESIS"
        })
        save_state()

def mine():
    while True:
        time.sleep(BLOCK_TIME)
        apply_flux_all()
        prev = chain[-1]
        block = {
            "index": len(chain),
            "timestamp": time.time(),
            "transactions": mempool.copy(),
            "prev_hash": prev["hash"]
        }
        block["hash"] = sha256(json.dumps(block, sort_keys=True))
        chain.append(block)
        mempool.clear()
        save_state()
        print(f"[MINED] Bloc {block['index']}")

# ==============================
# WALLET ECONOMIE
# ==============================
def apply_flux(wallet_id):
    w = wallets[wallet_id]
    month = time.strftime("%Y-%m")
    if "last_month" not in w or w["last_month"] != month:
        if w["status"] == "child":
            amount, ratio = CHILD_MONTHLY, CHILD_USABLE
        elif w["status"] == "ado":
            amount, ratio = ADO_MONTHLY, ADO_USABLE
        else:
            amount, ratio = ADULT_MONTHLY, ADULT_USABLE

        usable = amount * ratio
        w["balance"] += amount
        w["usable"] += usable
        w["locked"] += amount - usable
        w["age"] += 1

        # Passage child → ado → adult
        if w["status"] == "child" and w["age"] >= 18:
            w["status"] = "ado"
        elif w["status"] == "ado" and w["age"] >= 36:
            w["status"] = "adult"

        w["last_month"] = month

def apply_flux_all():
    for wid in wallets:
        apply_flux(wid)
    save_state()

# ==============================
# TRANSACTIONS SIGNÉES
# ==============================
def verify_tx(tx):
    try:
        sender = tx["from"]
        msg = f'{tx["from"]}{tx["to"]}{tx["amount"]}{tx["nonce"]}'
        sig = bytes.fromhex(tx["signature"])
        vk = VerifyKey(sender, encoder=HexEncoder)
        vk.verify(msg.encode(), sig)

        if wallets[sender]["usable"] < tx["amount"]:
            return False
        if nonces.get(sender, -1) >= tx["nonce"]:
            return False
        return True
    except:
        return False

def apply_tx(tx):
    sender, to, amount = tx["from"], tx["to"], tx["amount"]
    wallets[sender]["usable"] -= amount
    wallets[sender]["balance"] -= amount
    wallets[to]["balance"] += amount
    wallets[to]["usable"] += amount
    nonces[sender] = tx["nonce"]
    mempool.append(tx)
    save_state()

# ==============================
# WALLET CREATION
# ==============================
@app.route("/wallet/create", methods=["POST"])
def api_create_wallet():
    sk = SigningKey.generate()
    vk = sk.verify_key.encode(encoder=HexEncoder).decode()
    wallets[vk] = {
        "balance": 0,
        "usable": 0,
        "locked": 0,
        "status": "adult",
        "age": 0,
        "last_month": ""
    }
    apply_flux(vk)
    save_state()
    return jsonify({"wallet": vk, "sk": sk.encode(encoder=HexEncoder).decode()})

@app.route("/wallet/<wid>")
def wallet_view(wid):
    return jsonify(wallets.get(wid, {}))

@app.route("/chain")
def view_chain():
    return jsonify(chain)

@app.route("/wallet/ui/<wid>")
def wallet_ui(wid):
    w = wallets.get(wid)
    if not w:
        return "Wallet inconnu"
    html = """
    <body style="background:#111;color:#0f0;font-family:Arial;padding:20px">
    <h2>BASE Wallet</h2>
    <p>ID: {{ wid }}</p>
    <p>Status: {{ w.status }}</p>
    <p>Solde: {{ w.balance }}</p>
    <p>Utilisable: {{ w.usable }}</p>
    <p>Bloqué: {{ w.locked }}</p>
    </body>
    """
    return render_template_string(html, wid=wid, w=w)

# ==============================
# RUN NODE
# ==============================
if __name__ == "__main__":
    load_state()
    genesis()
    Thread(target=mine, daemon=True).start()
    print("NODE BASE prêt sur http://127.0.0.1:5000")
    serve(app, host="0.0.0.0", port=5000)
