from flask import Flask, request, jsonify
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)

DB = "events.db"


def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(
        eventId TEXT PRIMARY KEY,
        type TEXT,
        tenantId TEXT,
        severity TEXT,
        message TEXT,
        source TEXT,
        occurredAt TEXT,
        storedAt TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "skynet-ops-audit-service",
        "timestamp": datetime.utcnow()
    })


@app.route("/events", methods=["POST"])
def create_event():
    data = request.json

    required = ["type", "tenantId", "severity", "message", "source"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} required"}), 400

    if data["severity"] not in ["info", "warning", "error", "critical"]:
        return jsonify({"error": "invalid severity"}), 400

    event_id = str(uuid.uuid4())
    stored_at = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO events VALUES (?,?,?,?,?,?,?,?)
    """, (
        event_id,
        data["type"],
        data["tenantId"],
        data["severity"],
        data["message"],
        data["source"],
        data.get("occurredAt"),
        stored_at
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "eventId": event_id,
        "storedAt": stored_at
    }), 201


@app.route("/events", methods=["GET"])
def get_events():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events ORDER BY storedAt DESC")

    rows = cursor.fetchall()

    events = []

    for r in rows:
        events.append({
            "eventId": r[0],
            "type": r[1],
            "tenantId": r[2],
            "severity": r[3],
            "message": r[4],
            "source": r[5],
            "occurredAt": r[6],
            "storedAt": r[7]
        })

    conn.close()

    return jsonify(events)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
