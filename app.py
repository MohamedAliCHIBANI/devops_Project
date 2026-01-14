import logging
import uuid
import time
import random
from flask import Flask, jsonify, request, g, has_request_context
from prometheus_flask_exporter import PrometheusMetrics

# 1. Correction du Logging : Injecter trace_id en toute sécurité
old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    # Si on est dans une requête, on prend l'ID, sinon on met 'SYSTEM'
    if has_request_context():
        record.trace_id = getattr(g, 'trace_id', 'N/A')
    else:
        record.trace_id = 'SYSTEM'
    return record

logging.setLogRecordFactory(record_factory)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s service="backend" trace_id=%(trace_id)s message="%(message)s"')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 2. Setup Metrics (Prometheus)
metrics = PrometheusMetrics(app)

# Middleware: Ajouter un Trace ID unique à chaque requête
@app.before_request
def before_request():
    g.trace_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

@app.route('/')
def home():
    logger.info("Home endpoint called")
    return jsonify({"message": "DevOps Project API", "status": "running", "trace_id": g.trace_id})

@app.route('/api/data')
def get_data():
    time.sleep(random.uniform(0.1, 0.5))
    logger.info("Data endpoint called")
    return jsonify({"data": [1, 2, 3, 4, 5], "user": "student", "trace_id": g.trace_id})

@app.route('/api/error')
def trigger_error():
    logger.error("Error endpoint triggered")
    return jsonify({"error": "Something went wrong", "trace_id": g.trace_id}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)