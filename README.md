# VitaCare

### Agentic AI for Emergency Hospital Resource Allocation

**Smart Care. Saving Lives Faster.**

</div>

---

## The Problem

Every minute matters in a medical emergency. When a patient collapses, three critical decisions must be made simultaneously — **which hospital has beds**, **which ambulance is closest**, and **how critical is the patient**. These decisions are currently made manually, under pressure, with incomplete information.

VitaCare solves this with a **5-agent AI system** that makes all three decisions in under 2 seconds, explains its reasoning, and keeps every hospital and ambulance in sync in real time.

---

## Demo

```
Patient collapses
       ↓
Paramedic enters symptoms + severity
       ↓
AI Triage Agent     → Priority: CRITICAL (Score 9.2/10)
AI Allocation Agent → Best hospital: Apollo (8 ICU beds, 12 min away)
AI Routing Agent    → Nearest ambulance: VCA-002 (ETA 4 min)
AI Prediction Agent → Demand spike in 2 hours — pre-position 2 ambs
Coordination Agent  → Final decision + full explanation to dashboard
       ↓
Hospital pre-alerted via WebSocket
Bed reserved before ambulance arrives
```

---

## Features

### Web Dashboard
- **Live map** — color-coded hospital markers (green/amber/red) on dark CartoDB tiles
- **Hospital Resource Panel** — beds, ICU, ventilators, oxygen %, doctors, wait time, departments
- **Triage page** — full-screen patient intake form with AI decision shown side-by-side
- **Ambulance panel** — live status, patient priority badge, direct call button per driver
- **Alert ticker** — scrolling real-time critical alerts with buzzer sound
- **6-hour demand forecast** — bar chart with ICU/oxygen/ambulance risk indicators

### Mobile App (`/mobile`)
- Built for ambulance drivers on phone browsers
- One-tap hospital and driver call
- Quick patient register → AI triage
- Status toggle (Available / En Route / Busy)
- Live hospital bed counts and alerts

### AI Agent System

| Agent | What it does |
|-------|-------------|
| `TriageAgent` | Classifies severity Critical / Moderate / Mild using symptom keyword matching + score weighting |
| `AllocationAgent` | Scores every hospital on distance, ICU availability, wait time, oxygen, specialty match |
| `RoutingAgent` | Assigns nearest available ambulance, estimates ETA, prefers vitals-monitor units for Critical |
| `PredictionAgent` | Forecasts 6-hour patient demand with rush-hour multipliers, flags resource shortfall risk |
| `CoordinationAgent` | Master orchestrator — runs all agents in sequence, produces single decision with full explanation |

---

## Quick Start

### Prerequisites
- Python 3.9+
- VSCode (recommended)
- No Node.js required

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/ernandhinni/vitacare.git
cd vitacare

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate        # Mac / Linux
# venv\Scripts\activate         # Windows

# 4. Install dependencies
pip install flask flask-socketio eventlet

# 5. Run
python3 app.py
```

### Open in browser

```
Web Dashboard  →  http://127.0.0.1:5000
Mobile App     →  http://127.0.0.1:5000/mobile
```

The terminal also prints your **LAN IP** so phones on the same WiFi can open the mobile app directly.

---

## Project Structure

```
vitacare/
│
├── app.py                          ← Flask server, all API routes, WebSocket
├── requirements.txt
│
├── agents/
│   ├── triage_agent.py             ← Symptom keyword matching, severity scoring
│   ├── allocation_agent.py         ← Hospital scoring: distance / ICU / oxygen formula
│   ├── routing_agent.py            ← Ambulance assignment + ETA calculation
│   ├── prediction_agent.py         ← 6-hour demand forecasting with rush-hour model
│   └── coordination_agent.py       ← Master agent, orchestrates all sub-agents
│
├── data/
│   └── mock_data.py                ← 5 Bangalore hospitals, 5 ambulances, seed patients
│
├── templates/
│   ├── dashboard.html              ← Full web dashboard (map + triage + hospital panel)
│   └── mobile.html                 ← Mobile app for ambulance drivers
│
└── static/
    └── assets/
        └── logo.png
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/hospitals` | All hospitals with full resource data |
| `GET` | `/api/hospital/<id>` | Single hospital detail |
| `GET` | `/api/ambulances` | All ambulances + live status |
| `GET` | `/api/patients` | Registered patients |
| `POST` | `/api/triage` | Submit patient → full AI decision |
| `GET` | `/api/alerts` | Active system alerts |
| `GET` | `/api/predictions` | 6-hour demand forecast |
| `GET` | `/api/stats` | System-wide summary statistics |
| `GET` | `/api/server-info` | Returns LAN IP for mobile access |

### Triage request example

```json
POST /api/triage
{
  "name": "Arjun Menon",
  "age": 58,
  "blood_group": "B+",
  "symptoms": "chest pain, shortness of breath",
  "severity": 9,
  "medical_history": "Hypertension, Diabetes",
  "location": { "lat": 12.9400, "lng": 77.6100 }
}
```

```json
Response:
{
  "triage": { "priority": "Critical", "score": 9.2, "response_time": "< 5 minutes" },
  "allocation": { "hospital_name": "Apollo Emergency Center", "distance_km": 2.1, "icu_available": 8 },
  "routing": { "call_sign": "VCA-002", "eta_minutes": 4.3, "vitals_monitor": true },
  "master_explanation": "CRITICAL — Assigned to Apollo: 8 ICU beds, 2.1km away, ETA 4 min..."
}
```

---

## Real-time Events (WebSocket)

| Event | Payload | Trigger |
|-------|---------|---------|
| `hospitals_update` | Full hospital array | Every 8 seconds |
| `ambulances_update` | Full ambulance array | Every 8 seconds |
| `new_patient` | Patient object | After triage submission |
| `system_alert` | `{type, message, timestamp}` | ICU full, low beds, critical vitals |

---

## How the AI scoring works

### Hospital allocation formula (Critical patient)

```
score = distance_score × 0.25
      + icu_score       × 0.30   ← highest weight for critical
      + bed_score       × 0.15
      + wait_score      × 0.15
      + oxygen_score    × 0.10
      + specialty_score × 0.05
```

Critical patients with zero ICU beds are automatically excluded. The system reallocates to the next best hospital and explains the decision.

### Triage severity scoring

```
combined = (user_severity × 0.5) + (symptom_keyword_score × 0.5)
         + age_modifier    (±1.0 if age < 10 or > 65)
         + history_modifier (+0.5 if cardiac / diabetes / hypertension)

combined ≥ 8.0  →  Critical  (response time < 5 min)
combined ≥ 5.0  →  Moderate  (response time < 15 min)
combined  < 5.0 →  Mild      (response time < 30 min)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.9 + Flask 3.0 |
| Real-time | Flask-SocketIO + Eventlet |
| Frontend | Vanilla HTML / CSS / JS (no build step) |
| Map | Leaflet.js + CartoDB dark tiles |
| Charts | Chart.js |
| Fonts | Syne + DM Sans + JetBrains Mono (Google Fonts) |

Zero Node.js. Zero npm. Zero webpack. Pure Python backend + plain browser frontend.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgements

Built with [Flask](https://flask.palletsprojects.com), [Leaflet.js](https://leafletjs.com), [Chart.js](https://chartjs.org), [Socket.IO](https://socket.io), and [CartoDB](https://carto.com) map tiles.

Problem statement: Agentic AI for Emergency Hospital Resource Allocation.

---

<div align="center">

**VitaCare — Smart Care. Saving Lives Faster.**

Made with purpose.

</div>
