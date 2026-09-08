import random
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

TIPS = [
    "Containers should be stateless. If it needs to remember, it needs a volume.",
    "A pod is not a VM. Stop trying to SSH into it out of habit.",
    "If your Dockerfile has more than 10 layers, ask yourself why.",
    "YAML indentation errors are the #1 cause of 2am debugging sessions.",
    "Health checks aren't optional. They're how Kubernetes knows you're lying.",
    "Every replica is a promise. Kubernetes just keeps it.",
    "'It works on my machine' is not a deployment strategy.",
    "A Secret is just a ConfigMap wearing a disguise.",
    "The best time to write documentation was during the bug. The second best time is now.",
    "CI/CD doesn't remove human error. It just catches it faster.",
]

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Wisdom</title>
    <style>
        body {
            font-family: -apple-system, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: #1e293b;
            padding: 2.5rem;
            border-radius: 12px;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }
        h1 { font-size: 1rem; color: #64748b; text-transform: uppercase; letter-spacing: 2px; }
        p { font-size: 1.3rem; line-height: 1.5; min-height: 4.5rem; }
        small { color: #64748b; display: block; margin-bottom: 1.5rem; }
        button {
            background: #38bdf8;
            border: none;
            color: #0f172a;
            padding: 0.7rem 1.5rem;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            font-size: 1rem;
        }
        button:hover { background: #0ea5e9; }
    </style>
</head>
<body>
    <div class="card">
        <h1>DevOps Wisdom</h1>
        <p id="tip">{{ tip }}</p>
        <small id="served_at">Served at {{ served_at }}</small>
        <button onclick="getNewTip()">New Tip</button>
    </div>

    <script>
        async function getNewTip() {
            const response = await fetch('/api/tip');
            const data = await response.json();
            document.getElementById('tip').innerText = data.tip;
            document.getElementById('served_at').innerText = 'Served at ' + data.served_at;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    tip = random.choice(TIPS)
    served_at = datetime.now(timezone.utc).isoformat()
    return render_template_string(PAGE, tip=tip, served_at=served_at)

@app.route("/api/tip")
def api_tip():
    tip = random.choice(TIPS)
    served_at = datetime.now(timezone.utc).isoformat()
    return jsonify({"tip": tip, "served_at": served_at})

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
