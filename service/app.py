from flask import Flask, request, jsonify
import sqlite3
import uuid
from datetime import datetime
import os
import time
import random
import logging
import re

app = Flask(__name__)

# Environment configuration
DB = os.getenv("STORE_BACKEND", "events.db")
PORT = int(os.getenv("PORT", 3000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("audit-service")


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
        metadata TEXT,
        traceId TEXT,
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
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("NODE_ENV", "development")
    })


@app.route("/events", methods=["POST"])
def create_event():

    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()

    required = ["type", "tenantId", "severity", "message", "source"]

    for field in required:
        if field not in data or not data[field]:
            return jsonify({"error": f"{field} required"}), 400

    # enforce snake_case for type
    if not re.match(r"^[a-z0-9_]+$", data["type"]):
        return jsonify({"error": "type must be snake_case"}), 400

    if data["severity"] not in ["info", "warning", "error", "critical"]:
        return jsonify({"error": "invalid severity"}), 400

    event_id = str(uuid.uuid4())
    stored_at = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (
        event_id,
        data["type"],
        data["tenantId"],
        data["severity"],
        data["message"],
        data["source"],
        str(data.get("metadata")),
        data.get("traceId"),
        data.get("occurredAt"),
        stored_at
    ))

    conn.commit()
    conn.close()

    logger.info({
        "event": "event_ingested",
        "eventId": event_id,
        "tenantId": data["tenantId"],
        "severity": data["severity"]
    })

    return jsonify({
        "eventId": event_id,
        "storedAt": stored_at
    }), 201


@app.route("/events", methods=["GET"])
def get_events():

    tenant_id = request.args.get("tenantId")
    severity = request.args.get("severity")
    event_type = request.args.get("type")

    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))

    if limit > 100:
        limit = 100

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    if tenant_id:
        query += " AND tenantId = ?"
        params.append(tenant_id)

    if severity:
        query += " AND severity = ?"
        params.append(severity)

    if event_type:
        query += " AND type = ?"
        params.append(event_type)

    query += " ORDER BY storedAt DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
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
            "metadata": r[6],
            "traceId": r[7],
            "occurredAt": r[8],
            "storedAt": r[9]
        })

    conn.close()

    return jsonify(events)


@app.route("/metrics-demo", methods=["GET"])
def metrics_demo():

    mode = request.args.get("mode")

    if mode == "error":
        logger.error("Simulated error triggered")
        return jsonify({"error": "Simulated error"}), 500

    if mode == "slow":
        delay = random.randint(1, 3)
        logger.info(f"Simulated slow request ({delay}s)")
        time.sleep(delay)
        return jsonify({"message": f"Slow response ({delay}s)"})

    if mode == "burst":
        for i in range(20):
            logger.info(f"burst_event_{i}")
        return jsonify({"message": "Generated burst logs"})

    return jsonify({"message": "metrics demo endpoint"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)