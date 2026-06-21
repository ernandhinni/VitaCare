"""
VitaCare Mock Data - Hospitals, Ambulances, Patients
"""
from datetime import datetime

hospitals_db = {
    "H001": {
        "id": "H001", "name": "Apollo Emergency Center",
        "lat": 12.9352, "lng": 77.6245,
        "status": "Available",
        "total_beds": 120, "available_beds": 45,
        "icu_total": 20, "icu_available": 8,
        "ventilators": 12, "ventilators_available": 5,
        "oxygen_level": 85,
        "doctors_on_duty": 14,
        "emergency_staff": 22,
        "avg_wait_time": 12,
        "departments": {
            "Cardiology": {"capacity": 20, "current": 15},
            "Neurology": {"capacity": 15, "current": 10},
            "Orthopedics": {"capacity": 18, "current": 12},
            "Trauma": {"capacity": 25, "current": 18},
            "Pediatrics": {"capacity": 15, "current": 8}
        },
        "specialties": ["Cardiology", "Neurology", "Trauma", "Burns"],
        "phone": "+91-80-2345-6789",
        "address": "Bannerghatta Road, Bangalore",
        "rating": 4.6,
        "total_reviews": 1284,
        "top_doctors": [
            {"name": "Dr. Ramesh Iyer", "specialty": "Interventional Cardiology", "experience": "22 yrs", "rating": 4.9},
            {"name": "Dr. Sunita Pillai", "specialty": "Neurosurgery", "experience": "18 yrs", "rating": 4.8},
            {"name": "Dr. Arjun Das", "specialty": "Trauma & Critical Care", "experience": "14 yrs", "rating": 4.7}
        ],
        "reviews": [
            {"author": "Meena S.", "rating": 5, "date": "Mar 2025", "text": "Exceptional cardiac care. Dr. Iyer saved my father's life within minutes of arrival. Highly organised emergency wing."},
            {"author": "Kiran R.", "rating": 4, "date": "Feb 2025", "text": "Fast response, clean facility. Wait time was a bit longer than expected but staff were very attentive."},
            {"author": "Priya V.", "rating": 5, "date": "Jan 2025", "text": "Best emergency care in Bangalore. ICU team was outstanding. Would highly recommend."},
            {"author": "Suresh M.", "rating": 4, "date": "Dec 2024", "text": "Good doctors but parking is very difficult. The neurology department handled my case expertly."}
        ],
        "established": "1994",
        "accreditation": "NABH, JCI",
        "emergency_response": "< 5 min"
    },
    "H002": {
        "id": "H002", "name": "Manipal Hospital North",
        "lat": 12.9716, "lng": 77.5946,
        "status": "Limited",
        "total_beds": 200, "available_beds": 12,
        "icu_total": 30, "icu_available": 2,
        "ventilators": 20, "ventilators_available": 1,
        "oxygen_level": 72,
        "doctors_on_duty": 18,
        "emergency_staff": 30,
        "avg_wait_time": 28,
        "departments": {
            "Cardiology": {"capacity": 30, "current": 29},
            "Oncology": {"capacity": 25, "current": 23},
            "Nephrology": {"capacity": 20, "current": 19},
            "Trauma": {"capacity": 35, "current": 32},
            "Gynecology": {"capacity": 20, "current": 15}
        },
        "specialties": ["Oncology", "Cardiology", "Nephrology"],
        "phone": "+91-80-3456-7890",
        "address": "Old Airport Road, Bangalore",
        "rating": 4.3,
        "total_reviews": 976,
        "top_doctors": [
            {"name": "Dr. Kavitha Nair", "specialty": "Oncology", "experience": "20 yrs", "rating": 4.8},
            {"name": "Dr. Mohan Reddy", "specialty": "Nephrology", "experience": "16 yrs", "rating": 4.6},
            {"name": "Dr. Anil Sharma", "specialty": "Cardiology", "experience": "12 yrs", "rating": 4.5}
        ],
        "reviews": [
            {"author": "Ravi T.", "rating": 4, "date": "Mar 2025", "text": "Very good oncology department. Dr. Kavitha is thorough and compassionate. Recommend for cancer treatment."},
            {"author": "Leela K.", "rating": 3, "date": "Feb 2025", "text": "Long wait times in emergency but doctors are knowledgeable. Beds are limited right now."},
            {"author": "Ajay P.", "rating": 5, "date": "Jan 2025", "text": "Kidney treatment was world class. Dr. Mohan explained everything clearly. Facilities are top notch."},
            {"author": "Nalini B.", "rating": 4, "date": "Nov 2024", "text": "Good hospital overall. Staff could be more responsive but medical care quality is high."}
        ],
        "established": "2001",
        "accreditation": "NABH",
        "emergency_response": "< 10 min"
    },
    "H003": {
        "id": "H003", "name": "Fortis Emergency Wing",
        "lat": 12.9008, "lng": 77.6500,
        "status": "Available",
        "total_beds": 150, "available_beds": 67,
        "icu_total": 25, "icu_available": 12,
        "ventilators": 18, "ventilators_available": 9,
        "oxygen_level": 91,
        "doctors_on_duty": 20,
        "emergency_staff": 35,
        "avg_wait_time": 8,
        "departments": {
            "Cardiology": {"capacity": 25, "current": 12},
            "Orthopedics": {"capacity": 30, "current": 18},
            "Neurology": {"capacity": 20, "current": 11},
            "Trauma": {"capacity": 40, "current": 22},
            "Pediatrics": {"capacity": 20, "current": 14}
        },
        "specialties": ["Orthopedics", "Neurology", "Trauma", "Pediatrics"],
        "phone": "+91-80-4567-8901",
        "address": "Cunningham Road, Bangalore",
        "rating": 4.7,
        "total_reviews": 1542,
        "top_doctors": [
            {"name": "Dr. Vikram Menon", "specialty": "Orthopedic Surgery", "experience": "25 yrs", "rating": 4.9},
            {"name": "Dr. Deepa Krishnan", "specialty": "Pediatric Emergency", "experience": "15 yrs", "rating": 4.8},
            {"name": "Dr. Suhas Rao", "specialty": "Trauma Surgery", "experience": "19 yrs", "rating": 4.7}
        ],
        "reviews": [
            {"author": "Ganesh N.", "rating": 5, "date": "Apr 2025", "text": "Fastest emergency response I have ever seen. Orthopedic team was brilliant after my accident. Fully recovered."},
            {"author": "Saranya K.", "rating": 5, "date": "Mar 2025", "text": "Brought my son here after a fall. Dr. Deepa was amazing with kids. Very calm and reassuring. 10/10."},
            {"author": "Balaji V.", "rating": 4, "date": "Feb 2025", "text": "Great trauma team. A bit expensive but you get what you pay for. Clean rooms and attentive nurses."},
            {"author": "Rekha M.", "rating": 5, "date": "Jan 2025", "text": "Dr. Vikram performed knee surgery perfectly. No complications. Follow-up care was excellent too."}
        ],
        "established": "1998",
        "accreditation": "NABH, ISO 9001",
        "emergency_response": "< 4 min"
    },
    "H004": {
        "id": "H004", "name": "Victoria Government Hospital",
        "lat": 12.9634, "lng": 77.5855,
        "status": "Full",
        "total_beds": 300, "available_beds": 0,
        "icu_total": 40, "icu_available": 0,
        "ventilators": 25, "ventilators_available": 0,
        "oxygen_level": 45,
        "doctors_on_duty": 25,
        "emergency_staff": 50,
        "avg_wait_time": 55,
        "departments": {
            "General": {"capacity": 100, "current": 100},
            "Surgery": {"capacity": 80, "current": 80},
            "Pediatrics": {"capacity": 60, "current": 60},
            "Maternity": {"capacity": 60, "current": 60}
        },
        "specialties": ["General", "Surgery", "Pediatrics"],
        "phone": "+91-80-5678-9012",
        "address": "K R Road, Bangalore",
        "rating": 3.8,
        "total_reviews": 2341,
        "top_doctors": [
            {"name": "Dr. Prakash Shetty", "specialty": "General Surgery", "experience": "30 yrs", "rating": 4.6},
            {"name": "Dr. Geetha Anand", "specialty": "Obstetrics & Gynecology", "experience": "22 yrs", "rating": 4.5},
            {"name": "Dr. Venkat Rao", "specialty": "Pediatrics", "experience": "18 yrs", "rating": 4.4}
        ],
        "reviews": [
            {"author": "Muniraju S.", "rating": 4, "date": "Mar 2025", "text": "Government hospital doing its best under tough conditions. Doctors are dedicated and skilled despite resource constraints."},
            {"author": "Fatima B.", "rating": 3, "date": "Feb 2025", "text": "Very overcrowded but the staff try hard. Dr. Geetha was wonderful during my delivery. Long waits though."},
            {"author": "Ramu H.", "rating": 4, "date": "Jan 2025", "text": "Free treatment for those who need it. Dr. Prakash is excellent. Needs more funding and resources."},
            {"author": "Champa D.", "rating": 3, "date": "Dec 2024", "text": "Decent care given the patient load. Wish they had more beds. Nurses are hard working and caring."}
        ],
        "established": "1902",
        "accreditation": "Government Certified",
        "emergency_response": "< 20 min"
    },
    "H005": {
        "id": "H005", "name": "Narayana Hrudayalaya",
        "lat": 12.8956, "lng": 77.6387,
        "status": "Available",
        "total_beds": 180, "available_beds": 89,
        "icu_total": 35, "icu_available": 18,
        "ventilators": 22, "ventilators_available": 14,
        "oxygen_level": 95,
        "doctors_on_duty": 22,
        "emergency_staff": 40,
        "avg_wait_time": 6,
        "departments": {
            "Cardiac Surgery": {"capacity": 40, "current": 22},
            "Cardiology": {"capacity": 35, "current": 18},
            "Pediatric Cardiology": {"capacity": 25, "current": 12},
            "Vascular": {"capacity": 20, "current": 10},
            "Transplant": {"capacity": 15, "current": 7}
        },
        "specialties": ["Cardiac Surgery", "Cardiology", "Transplant", "Vascular"],
        "phone": "+91-80-6789-0123",
        "address": "Bommasandra, Bangalore",
        "rating": 4.9,
        "total_reviews": 3102,
        "top_doctors": [
            {"name": "Dr. Devi Prasad Shetty", "specialty": "Cardiac Surgery", "experience": "35 yrs", "rating": 5.0},
            {"name": "Dr. Anitha Kumar", "specialty": "Pediatric Cardiology", "experience": "20 yrs", "rating": 4.9},
            {"name": "Dr. Rajesh Nambiar", "specialty": "Vascular Surgery", "experience": "17 yrs", "rating": 4.8}
        ],
        "reviews": [
            {"author": "Chandru M.", "rating": 5, "date": "Apr 2025", "text": "World class cardiac care at affordable cost. Dr. Shetty is a legend. My bypass surgery was flawless."},
            {"author": "Indira V.", "rating": 5, "date": "Mar 2025", "text": "My daughter had a heart defect. Dr. Anitha performed the surgery perfectly. We are forever grateful."},
            {"author": "Rajan P.", "rating": 5, "date": "Feb 2025", "text": "Best cardiac hospital in South India without doubt. Compassionate staff, cutting edge technology."},
            {"author": "Suma T.", "rating": 4, "date": "Jan 2025", "text": "Excellent doctors and great post-op care. Location is a bit far but completely worth the distance."}
        ],
        "established": "2000",
        "accreditation": "NABH, JCI, NABL",
        "emergency_response": "< 3 min"
    }
}

ambulances_db = {
    "A001": {
        "id": "A001", "call_sign": "VCA-001",
        "lat": 12.9400, "lng": 77.6100,
        "status": "Available",
        "driver": "Ravi Kumar", "driver_phone": "+91-9876543210",
        "vitals_monitor": True,
        "patient": None, "destination": None,
        "eta": None, "speed": 0,
        "heart_rate": None, "oxygen_level": None
    },
    "A002": {
        "id": "A002", "call_sign": "VCA-002",
        "lat": 12.9750, "lng": 77.5800,
        "status": "En Route",
        "driver": "Suresh Nair", "driver_phone": "+91-9876543211",
        "vitals_monitor": True,
        "patient": "Meena Sharma", "destination": "H003",
        "eta": "7 mins", "speed": 65,
        "heart_rate": 102, "oxygen_level": 94
    },
    "A003": {
        "id": "A003", "call_sign": "VCA-003",
        "lat": 12.8900, "lng": 77.6400,
        "status": "Available",
        "driver": "Anand Raj", "driver_phone": "+91-9876543212",
        "vitals_monitor": True,
        "patient": None, "destination": None,
        "eta": None, "speed": 0,
        "heart_rate": None, "oxygen_level": None
    },
    "A004": {
        "id": "A004", "call_sign": "VCA-004",
        "lat": 12.9600, "lng": 77.6200,
        "status": "Busy",
        "driver": "Priya Das", "driver_phone": "+91-9876543213",
        "vitals_monitor": True,
        "patient": "Kiran Patel", "destination": "H001",
        "eta": "3 mins", "speed": 72,
        "heart_rate": 88, "oxygen_level": 97
    },
    "A005": {
        "id": "A005", "call_sign": "VCA-005",
        "lat": 12.9100, "lng": 77.5700,
        "status": "Available",
        "driver": "Mohammed Ali", "driver_phone": "+91-9876543214",
        "vitals_monitor": False,
        "patient": None, "destination": None,
        "eta": None, "speed": 0,
        "heart_rate": None, "oxygen_level": None
    }
}

patients_db = {
    "P0001": {
        "id": "P0001",
        "name": "Arjun Menon",
        "age": 58,
        "blood_group": "B+",
        "medical_history": "Hypertension, Diabetes",
        "symptoms": "Chest pain, shortness of breath",
        "severity": 9,
        "priority": "Critical",
        "assigned_hospital": "H001",
        "assigned_ambulance": "A002",
        "timestamp": datetime.now().isoformat(),
        "status": "En Route",
        "location": {"lat": 12.9380, "lng": 77.6150},
        "ai_decision": {
            "explanation": "Assigned to Apollo Emergency Center: 8 ICU beds available, nearest cardiac unit, 12 min ETA"
        }
    },
    "P0002": {
        "id": "P0002",
        "name": "Lakshmi Iyer",
        "age": 34,
        "blood_group": "A+",
        "medical_history": "None",
        "symptoms": "Road accident, fractures",
        "severity": 7,
        "priority": "Moderate",
        "assigned_hospital": "H003",
        "assigned_ambulance": "A004",
        "timestamp": datetime.now().isoformat(),
        "status": "En Route",
        "location": {"lat": 12.9620, "lng": 77.6210},
        "ai_decision": {
            "explanation": "Assigned to Fortis Emergency Wing: Best orthopedic unit, 8 min ETA, lowest wait time"
        }
    }
}
