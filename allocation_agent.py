"""
Allocation Agent - Assigns best hospital based on patient needs and resources
"""
import math

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

class AllocationAgent:
    def __init__(self, hospitals_db):
        self.hospitals = hospitals_db

    def allocate(self, patient_location: dict, priority: str, symptoms: str, specialties_needed: list = None) -> dict:
        scores = []
        lat, lng = patient_location['lat'], patient_location['lng']

        for hid, h in self.hospitals.items():
            if h['status'] == 'Full':
                continue
            if h['available_beds'] == 0:
                continue

            distance = haversine(lat, lng, h['lat'], h['lng'])
            distance_score = max(0, 10 - distance * 2)

            bed_ratio = h['available_beds'] / h['total_beds']
            bed_score = bed_ratio * 10

            icu_score = 0
            if priority == 'Critical':
                if h['icu_available'] > 0:
                    icu_score = min(10, h['icu_available'] * 2)
                else:
                    continue  # Critical needs ICU

            wait_score = max(0, 10 - h['avg_wait_time'] / 5)
            oxygen_score = h['oxygen_level'] / 10

            specialty_score = 0
            if specialties_needed:
                hospital_specs = [s.lower() for s in h.get('specialties', [])]
                for spec in specialties_needed:
                    if spec.lower() in hospital_specs:
                        specialty_score += 5

            # Weighted composite score
            if priority == 'Critical':
                total = (distance_score * 0.25 + icu_score * 0.30 +
                         bed_score * 0.15 + wait_score * 0.15 +
                         oxygen_score * 0.10 + specialty_score * 0.05)
            elif priority == 'Moderate':
                total = (distance_score * 0.35 + bed_score * 0.25 +
                         wait_score * 0.20 + oxygen_score * 0.10 +
                         specialty_score * 0.10)
            else:
                total = (distance_score * 0.40 + bed_score * 0.30 +
                         wait_score * 0.20 + oxygen_score * 0.10)

            scores.append({
                'hospital_id': hid,
                'hospital_name': h['name'],
                'total_score': round(total, 2),
                'distance_km': round(distance, 1),
                'available_beds': h['available_beds'],
                'icu_available': h['icu_available'],
                'avg_wait_time': h['avg_wait_time'],
                'oxygen_level': h['oxygen_level'],
                'breakdown': {
                    'distance_score': round(distance_score, 1),
                    'bed_score': round(bed_score, 1),
                    'icu_score': round(icu_score, 1),
                    'wait_score': round(wait_score, 1),
                    'oxygen_score': round(oxygen_score, 1),
                    'specialty_score': round(specialty_score, 1)
                }
            })

        if not scores:
            # Fallback: pick hospital with most beds
            best = max(self.hospitals.values(), key=lambda h: h['available_beds'])
            return {
                'hospital_id': best['id'],
                'hospital_name': best['name'],
                'distance_km': round(haversine(lat, lng, best['lat'], best['lng']), 1),
                'available_beds': best['available_beds'],
                'icu_available': best['icu_available'],
                'avg_wait_time': best['avg_wait_time'],
                'total_score': 0,
                'alternatives': [],
                'explanation': f"Fallback allocation to {best['name']} (best available capacity)"
            }

        scores.sort(key=lambda x: x['total_score'], reverse=True)
        best = scores[0]
        alternatives = scores[1:3]

        reasons = []
        if best['icu_available'] > 0:
            reasons.append(f"{best['icu_available']} ICU beds available")
        reasons.append(f"{best['distance_km']} km away (~{int(best['distance_km']*2)} min ETA)")
        reasons.append(f"{best['available_beds']} general beds free")
        if best['avg_wait_time'] < 15:
            reasons.append(f"Low wait time ({best['avg_wait_time']} min)")
        reasons.append(f"Oxygen at {best['oxygen_level']}%")

        return {
            **best,
            'alternatives': alternatives,
            'explanation': f"Assigned to {best['hospital_name']} because: " + ", ".join(reasons)
        }
