"""
Triage Agent - Classifies patient severity and assigns priority
"""

SYMPTOM_WEIGHTS = {
    # Critical symptoms
    'chest pain': 9, 'cardiac arrest': 10, 'stroke': 10, 'unconscious': 10,
    'not breathing': 10, 'severe bleeding': 9, 'head trauma': 9,
    'anaphylaxis': 9, 'seizure': 8, 'overdose': 9,
    # Moderate symptoms
    'shortness of breath': 7, 'fracture': 6, 'high fever': 6,
    'severe pain': 6, 'vomiting blood': 8, 'burns': 7, 'allergic': 6,
    # Mild symptoms
    'fever': 4, 'nausea': 3, 'mild pain': 3, 'sprain': 3,
    'headache': 3, 'cough': 2, 'rash': 2, 'dizziness': 4
}

class TriageAgent:
    def classify(self, symptoms: str, severity: int, age: int = 30, medical_history: str = "") -> dict:
        symptoms_lower = symptoms.lower()
        symptom_score = 0
        matched = []

        for keyword, weight in SYMPTOM_WEIGHTS.items():
            if keyword in symptoms_lower:
                symptom_score = max(symptom_score, weight)
                matched.append(keyword)

        # Combine user-reported severity with AI symptom score
        combined = (severity * 0.5) + (symptom_score * 0.5)

        # Age modifiers
        if age > 65 or age < 10:
            combined += 1.0

        # Medical history modifiers
        hist_lower = medical_history.lower()
        if any(k in hist_lower for k in ['heart', 'cardiac', 'diabetes', 'hypertension']):
            combined += 0.5

        combined = min(combined, 10)

        if combined >= 8:
            priority = "Critical"
            color = "#FF3B3B"
            response_time = "< 5 minutes"
        elif combined >= 5:
            priority = "Moderate"
            color = "#FF9500"
            response_time = "< 15 minutes"
        else:
            priority = "Mild"
            color = "#34C759"
            response_time = "< 30 minutes"

        return {
            "priority": priority,
            "color": color,
            "score": round(combined, 1),
            "response_time": response_time,
            "matched_symptoms": matched,
            "explanation": (
                f"Severity score {round(combined,1)}/10. "
                f"Detected: {', '.join(matched) if matched else 'general complaint'}. "
                f"Required response time: {response_time}."
            )
        }
