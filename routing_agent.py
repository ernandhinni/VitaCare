"""
Routing Agent - Assigns nearest ambulance and estimates arrival time
"""
import math

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

class RoutingAgent:
    def assign_ambulance(self, patient_location: dict, ambulances_db: dict, priority: str) -> dict:
        lat, lng = patient_location['lat'], patient_location['lng']
        available = [a for a in ambulances_db.values() if a['status'] == 'Available']

        if not available:
            return {
                'ambulance_id': 'NONE',
                'call_sign': 'N/A',
                'driver': 'No ambulance available',
                'eta_minutes': 999,
                'distance_km': 0,
                'explanation': 'No ambulances available - manual dispatch needed',
                'vitals_monitor': False
            }

        scored = []
        for amb in available:
            dist = haversine(lat, lng, amb['lat'], amb['lng'])
            # Prefer ambulances with vitals monitor for Critical
            monitor_bonus = 2 if (priority == 'Critical' and amb.get('vitals_monitor')) else 0
            score = 10 - dist * 3 + monitor_bonus
            speed_kmh = 60  # avg city speed with siren
            eta = (dist / speed_kmh) * 60  # minutes
            scored.append({
                'ambulance_id': amb['id'],
                'call_sign': amb['call_sign'],
                'driver': amb['driver'],
                'driver_phone': amb['driver_phone'],
                'distance_km': round(dist, 1),
                'eta_minutes': round(eta, 1),
                'score': round(score, 2),
                'vitals_monitor': amb.get('vitals_monitor', False),
                'driver_phone': amb.get('driver_phone', '')
            })

        scored.sort(key=lambda x: x['score'], reverse=True)
        best = scored[0]

        # Mark ambulance as En Route
        ambulances_db[best['ambulance_id']]['status'] = 'En Route'

        return {
            **best,
            'explanation': (
                f"Nearest available ambulance {best['call_sign']} assigned. "
                f"Distance: {best['distance_km']} km. "
                f"ETA: {best['eta_minutes']} min. "
                f"{'Vitals monitor equipped.' if best['vitals_monitor'] else ''}"
            )
        }
