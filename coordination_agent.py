"""
Coordination Agent (Master) - Orchestrates all sub-agents and makes final decisions
"""
from data.mock_data import ambulances_db

SPECIALTY_MAP = {
    'chest pain': ['Cardiology', 'Cardiac Surgery'],
    'cardiac arrest': ['Cardiology', 'Cardiac Surgery'],
    'stroke': ['Neurology'],
    'head trauma': ['Neurology', 'Trauma'],
    'fracture': ['Orthopedics'],
    'burns': ['Burns'],
    'pediatric': ['Pediatrics'],
    'cancer': ['Oncology'],
    'kidney': ['Nephrology'],
}

class CoordinationAgent:
    def __init__(self, triage_agent, allocation_agent, routing_agent, prediction_agent):
        self.triage = triage_agent
        self.allocation = allocation_agent
        self.routing = routing_agent
        self.prediction = prediction_agent

    def _detect_specialties(self, symptoms: str) -> list:
        symptoms_lower = symptoms.lower()
        needed = []
        for keyword, specs in SPECIALTY_MAP.items():
            if keyword in symptoms_lower:
                needed.extend(specs)
        return list(set(needed))

    def process_emergency(self, name, symptoms, severity, location,
                          blood_group='O+', medical_history='', age=30) -> dict:
        # Step 1: Triage
        triage_result = self.triage.classify(
            symptoms=symptoms, severity=severity,
            age=age, medical_history=medical_history
        )

        # Step 2: Detect specialties needed
        specialties = self._detect_specialties(symptoms)

        # Step 3: Allocate hospital
        allocation_result = self.allocation.allocate(
            patient_location=location,
            priority=triage_result['priority'],
            symptoms=symptoms,
            specialties_needed=specialties
        )

        # Step 4: Route ambulance
        routing_result = self.routing.assign_ambulance(
            patient_location=location,
            ambulances_db=ambulances_db,
            priority=triage_result['priority']
        )

        # Step 5: Master decision summary
        master_explanation = (
            f"VITACARE AI DECISION SUMMARY\n"
            f"Patient: {name} | Priority: {triage_result['priority']} | Score: {triage_result['score']}/10\n\n"
            f"TRIAGE: {triage_result['explanation']}\n\n"
            f"HOSPITAL: {allocation_result['explanation']}\n\n"
            f"AMBULANCE: {routing_result['explanation']}"
        )

        return {
            'triage': triage_result,
            'allocation': allocation_result,
            'routing': routing_result,
            'master_explanation': master_explanation,
            'specialties_needed': specialties,
            'patient_name': name
        }
