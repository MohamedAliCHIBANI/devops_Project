import logging
import uuid
import time
import random
from flask import Flask, jsonify, request, g, has_request_context
from prometheus_flask_exporter import PrometheusMetrics

# --- CONFIGURATION & LOGGING ---
# Custom Log Factory to inject Trace ID safely
old_factory = logging.getLogRecordFactory()
def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    if has_request_context():
        record.trace_id = getattr(g, 'trace_id', 'N/A')
    else:
        record.trace_id = 'SYSTEM'
    return record

logging.setLogRecordFactory(record_factory)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s service="backend" trace_id=%(trace_id)s message="%(message)s"')
logger = logging.getLogger(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# --- IN-MEMORY DATABASE ---
# Simple list to store todos
todos = [
    {"id": "1", "title": "Finish DevOps Project", "done": False},
    {"id": "2", "title": "Deploy to Kubernetes", "done": False}
]

# --- MIDDLEWARE ---
@app.before_request
def before_request():
    g.trace_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

# --- ROUTES ---

@app.route('/')
def home():
    logger.info("Home endpoint called")
    return jsonify({
        "message": "DevOps Project API v2", 
        "status": "running", 
        "trace_id": g.trace_id
    })

@app.route('/api/todos', methods=['GET'])
def get_todos():
    logger.info(f"Fetching {len(todos)} todos")
    return jsonify({"todos": todos, "count": len(todos)})

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        logger.warning("Invalid todo creation attempt")
        return jsonify({"error": "Title is required"}), 400
    
    new_todo = {
        "id": str(uuid.uuid4()),
        "title": data['title'],
        "done": False
    }
    todos.append(new_todo)
    logger.info(f"Todo created: {new_todo['id']}")
    return jsonify(new_todo), 201

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    initial_count = len(todos)
    todos = [t for t in todos if t['id'] != todo_id]
    
    if len(todos) < initial_count:
        logger.info(f"Todo deleted: {todo_id}")
        return jsonify({"message": "Deleted successfully"}), 200
    else:
        logger.warning(f"Todo not found for deletion: {todo_id}")
        return jsonify({"error": "Todo not found"}), 404

@app.route('/api/error')
def trigger_error():
    logger.error("Simulated error triggered")
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)