\
from flask import Flask, request, jsonify, render_template
import requests

APP_ID = "E6AC194E-095F-44F0-BF76-223C12EF6337"
REST_API_KEY = "557ADB02-52D8-422D-90EF-BDF931195F97"  
BASE = f"https://api.backendless.com/{APP_ID}/{REST_API_KEY}"

HEADERS = {"Content-Type": "application/json"}

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/subjects")
def list_subjects():
    url = f"{BASE}/data/Subjects"
    params = {"pageSize": 200, "offset": 0}
    print("→ GET", url, params, flush=True)
    r = requests.get(url, headers=HEADERS, params=params, timeout=20)
    if not r.ok:
        # Devuelve texto y código de Backendless para ver exactamente el problema
        print("← ERROR", r.status_code, r.text, flush=True)
        return {"error": True, "status": r.status_code, "backendless": r.text}, r.status_code
    data = r.json()
    # Asegura formato lista
    if isinstance(data, dict):
        data = [data]
    return jsonify(data)

@app.get("/api/subjects/by-code")
def get_by_code():
    code = request.args.get("code", "")
    r = requests.get(f"{BASE}/data/Subjects", headers=HEADERS, params={"where": f"code='{code}'", "pageSize": 1}, timeout=20)
    r.raise_for_status()
    items = r.json()
    return jsonify(items[0] if items else {}), 200

@app.post("/api/subjects")
def create_subject():
    data = request.get_json(force=True) or {}
    r = requests.post(f"{BASE}/data/Subjects", headers=HEADERS, json=data, timeout=20)
    r.raise_for_status()
    return jsonify(r.json()), 201

@app.put("/api/subjects/<object_id>")
def update_subject(object_id):
    data = request.get_json(force=True) or {}
    r = requests.put(f"{BASE}/data/Subjects/{object_id}", headers=HEADERS, json=data, timeout=20)
    r.raise_for_status()
    return jsonify(r.json()), 200

@app.delete("/api/subjects/<object_id>")
def delete_subject(object_id):
    r = requests.delete(f"{BASE}/data/Subjects/{object_id}", headers=HEADERS, timeout=20)
    if r.status_code in (200, 204):
        return "", 204
    return r.text, r.status_code

if __name__ == "__main__":
    app.run(port=8000, debug=True)
