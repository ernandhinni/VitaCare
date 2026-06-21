"""
VitaCare - Agentic AI for Emergency Hospital Resource Allocation
Main Flask Application
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json, random, time, threading
from datetime import datetime, timedelta
from agents.triage_agent import TriageAgent
from agents.allocation_agent import AllocationAgent
from agents.routing_agent import RoutingAgent
from agents.prediction_agent import PredictionAgent
from agents.coordination_agent import CoordinationAgent
from data.mock_data import hospitals_db, ambulances_db, patients_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vitacare-secret-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Agents
triage_agent = TriageAgent()
allocation_agent = AllocationAgent(hospitals_db)
routing_agent = RoutingAgent()
prediction_agent = PredictionAgent()
coordination_agent = CoordinationAgent(
    triage_agent, allocation_agent, routing_agent, prediction_agent
)

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

# ── Hospitals ──────────────────────────────────

@app.route('/api/hospitals', methods=['GET'])
def get_hospitals():
    return jsonify(list(hospitals_db.values()))

@app.route('/api/hospital/<hospital_id>', methods=['GET'])
def get_hospital(hospital_id):
    h = hospitals_db.get(hospital_id)
    if not h:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(h)

# ── Ambulances ─────────────────────────────────

@app.route('/api/ambulances', methods=['GET'])
def get_ambulances():
    return jsonify(list(ambulances_db.values()))

# ── Patients ───────────────────────────────────

@app.route('/api/patients', methods=['GET'])
def get_patients():
    return jsonify(list(patients_db.values()))

@app.route('/api/patient/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    p = patients_db.get(patient_id)
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(p)

# ── Triage & AI Decision ────────────────────────

@app.route('/api/triage', methods=['POST'])
def triage_patient():
    data = request.json
    name         = data.get('name', 'Unknown')
    symptoms     = data.get('symptoms', '')
    severity     = data.get('severity', 5)
    location     = data.get('location', {'lat': 12.9716, 'lng': 77.5946})
    blood_group  = data.get('blood_group', 'O+')
    medical_hist = data.get('medical_history', '')
    age          = data.get('age', 30)

    result = coordination_agent.process_emergency(
        name=name,
        symptoms=symptoms,
        severity=int(severity),
        location=location,
        blood_group=blood_group,
        medical_history=medical_hist,
        age=age
    )

    # Save patient
    pid = f"P{len(patients_db)+1:04d}"
    patients_db[pid] = {
        'id': pid,
        'name': name,
        'age': age,
        'blood_group': blood_group,
        'medical_history': medical_hist,
        'symptoms': symptoms,
        'severity': severity,
        'priority': result['triage']['priority'],
        'assigned_hospital': result['allocation']['hospital_id'],
        'assigned_ambulance': result['routing']['ambulance_id'],
        'timestamp': datetime.now().isoformat(),
        'status': 'En Route',
        'location': location,
        'ai_decision': result
    }

    # Broadcast update via WebSocket
    socketio.emit('new_patient', patients_db[pid])
    socketio.emit('system_alert', {
        'type': 'critical' if result['triage']['priority'] == 'Critical' else 'info',
        'message': f"New {result['triage']['priority']} patient assigned to {result['allocation']['hospital_name']}",
        'timestamp': datetime.now().isoformat()
    })

    return jsonify({'patient_id': pid, **result})

# ── Alerts ─────────────────────────────────────

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    alerts = []
    for hid, h in hospitals_db.items():
        if h['icu_available'] == 0:
            alerts.append({'type': 'critical', 'message': f"ICU FULL at {h['name']}", 'hospital_id': hid})
        if h['available_beds'] < 3:
            alerts.append({'type': 'warning', 'message': f"Low beds ({h['available_beds']}) at {h['name']}", 'hospital_id': hid})
        if h['oxygen_level'] < 30:
            alerts.append({'type': 'warning', 'message': f"Low oxygen at {h['name']}", 'hospital_id': hid})
    for aid, a in ambulances_db.items():
        if a['status'] == 'Delayed':
            alerts.append({'type': 'warning', 'message': f"Ambulance {a['id']} delay detected", 'ambulance_id': aid})
    return jsonify(alerts)

# ── Predictions ────────────────────────────────

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    preds = prediction_agent.forecast_demand()
    return jsonify(preds)

# ── Stats ──────────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_beds = sum(h['total_beds'] for h in hospitals_db.values())
    available_beds = sum(h['available_beds'] for h in hospitals_db.values())
    total_icu = sum(h['icu_total'] for h in hospitals_db.values())
    available_icu = sum(h['icu_available'] for h in hospitals_db.values())
    active_ambs = sum(1 for a in ambulances_db.values() if a['status'] == 'En Route')
    return jsonify({
        'total_hospitals': len(hospitals_db),
        'total_beds': total_beds,
        'available_beds': available_beds,
        'bed_occupancy_pct': round((total_beds - available_beds) / total_beds * 100, 1),
        'total_icu': total_icu,
        'available_icu': available_icu,
        'active_ambulances': active_ambs,
        'total_ambulances': len(ambulances_db),
        'patients_today': len(patients_db),
        'critical_patients': sum(1 for p in patients_db.values() if p.get('priority') == 'Critical'),
    })

# ── WebSocket ──────────────────────────────────

@socketio.on('connect')
def handle_connect():
    emit('connected', {'message': 'VitaCare connected'})

@socketio.on('request_update')
def handle_update():
    emit('hospitals_update', list(hospitals_db.values()))
    emit('ambulances_update', list(ambulances_db.values()))

# ── Live simulation thread ──────────────────────

def simulate_realtime():
    """Simulates live changes to hospital/ambulance data"""
    while True:
        time.sleep(8)
        # Randomly vary some hospital beds
        for hid, h in hospitals_db.items():
            delta = random.randint(-1, 1)
            h['available_beds'] = max(0, min(h['total_beds'], h['available_beds'] + delta))
            h['avg_wait_time'] = max(5, h['avg_wait_time'] + random.randint(-2, 2))

        # Randomly update ambulance status
        for aid, a in ambulances_db.items():
            if a['status'] == 'En Route' and random.random() < 0.3:
                a['status'] = 'Available'
                a['patient'] = None
            elif a['status'] == 'Available' and random.random() < 0.1:
                a['status'] = 'En Route'

        socketio.emit('hospitals_update', list(hospitals_db.values()))
        socketio.emit('ambulances_update', list(ambulances_db.values()))


@app.route('/api/server-info', methods=['GET'])
def server_info():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan_ip = s.getsockname()[0]
        s.close()
    except Exception:
        lan_ip = '127.0.0.1'
    return jsonify({'lan_ip': lan_ip, 'port': 5000})

if __name__ == '__main__':
    import socket as _sock
    try:
        _s = _sock.socket(_sock.AF_INET, _sock.SOCK_DGRAM)
        _s.connect(("8.8.8.8", 80))
        lan_ip = _s.getsockname()[0]
        _s.close()
    except Exception:
        lan_ip = '127.0.0.1'

    sim_thread = threading.Thread(target=simulate_realtime, daemon=True)
    sim_thread.start()

    print("\n" + "="*55)
    print("  VitaCare is RUNNING")
    print("="*55)
    print(f"  Web Dashboard  : http://127.0.0.1:5000")
    print(f"  Mobile (Phone) : http://{lan_ip}:5000/mobile")
    print(f"\n  On your phone open Safari/Chrome and type:")
    print(f"      http://{lan_ip}:5000/mobile")
    print(f"\n  Phone must be on the SAME WiFi as this Mac!")
    print("="*55 + "\n")
    socketio.run(app, debug=False, host='0.0.0.0', port=5000, use_reloader=False)
