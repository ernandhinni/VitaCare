"""
Prediction Agent - Forecasts demand spikes and resource shortfalls
"""
import random
from datetime import datetime, timedelta

class PredictionAgent:
    def forecast_demand(self) -> dict:
        now = datetime.now()
        hours = [(now + timedelta(hours=i)).strftime('%H:00') for i in range(6)]

        base_demand = [random.randint(3, 8) for _ in range(6)]
        # Peak hours: morning 8-10 and evening 18-20
        hour_now = now.hour
        if 8 <= hour_now <= 10 or 18 <= hour_now <= 20:
            base_demand[0] = random.randint(8, 15)

        forecasts = [
            {
                'hour': hours[i],
                'expected_patients': base_demand[i],
                'confidence': round(random.uniform(0.72, 0.95), 2)
            }
            for i in range(6)
        ]

        alerts = []
        if max(base_demand) > 10:
            alerts.append({
                'type': 'warning',
                'message': f"High demand spike predicted at {hours[base_demand.index(max(base_demand))]}",
                'action': 'Consider pre-positioning 2 additional ambulances'
            })

        resource_status = {
            'icu_risk': 'High' if random.random() > 0.6 else 'Medium',
            'ambulance_shortage_risk': 'Low' if random.random() > 0.7 else 'Medium',
            'oxygen_restock_needed': random.choice([True, False])
        }

        return {
            'forecast': forecasts,
            'alerts': alerts,
            'resource_status': resource_status,
            'generated_at': now.isoformat()
        }
