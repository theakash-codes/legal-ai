"""
Mock lawyer database for recommendations
"""
import math, random

LAWYERS = [
    {"name": "Adv. Rajesh Kumar Sharma", "specialty": "Property Law", "experience": 18, "rating": 4.8, "cases_won": 340, "phone": "+91 98765 43210", "photo_initials": "RS", "lat": 12.9716, "lng": 77.5946, "city": "Bangalore", "languages": ["English", "Hindi", "Kannada"], "fee": "₹2,500/consultation"},
    {"name": "Adv. Priya Nair", "specialty": "Family Law", "experience": 12, "rating": 4.9, "cases_won": 215, "phone": "+91 98765 43211", "photo_initials": "PN", "lat": 12.9352, "lng": 77.6245, "city": "Bangalore", "languages": ["English", "Malayalam", "Kannada"], "fee": "₹2,000/consultation"},
    {"name": "Adv. Suresh Reddy", "specialty": "Criminal Law", "experience": 22, "rating": 4.7, "cases_won": 480, "phone": "+91 98765 43212", "photo_initials": "SR", "lat": 12.9850, "lng": 77.6050, "city": "Bangalore", "languages": ["English", "Telugu", "Kannada"], "fee": "₹3,000/consultation"},
    {"name": "Adv. Meenakshi Iyer", "specialty": "Corporate Law", "experience": 15, "rating": 4.6, "cases_won": 190, "phone": "+91 98765 43213", "photo_initials": "MI", "lat": 13.0100, "lng": 77.5500, "city": "Bangalore", "languages": ["English", "Tamil", "Hindi"], "fee": "₹3,500/consultation"},
    {"name": "Adv. Arun Patel", "specialty": "Civil Law", "experience": 20, "rating": 4.8, "cases_won": 390, "phone": "+91 98765 43214", "photo_initials": "AP", "lat": 12.9600, "lng": 77.5700, "city": "Bangalore", "languages": ["English", "Gujarati", "Hindi"], "fee": "₹2,500/consultation"},
    {"name": "Adv. Kavitha Menon", "specialty": "Employment Law", "experience": 10, "rating": 4.5, "cases_won": 145, "phone": "+91 98765 43215", "photo_initials": "KM", "lat": 12.9400, "lng": 77.6100, "city": "Bangalore", "languages": ["English", "Malayalam"], "fee": "₹2,000/consultation"},
    {"name": "Adv. Vikram Singh", "specialty": "Property Law", "experience": 25, "rating": 4.9, "cases_won": 520, "phone": "+91 98765 43216", "photo_initials": "VS", "lat": 12.9800, "lng": 77.5800, "city": "Bangalore", "languages": ["English", "Hindi", "Punjabi"], "fee": "₹4,000/consultation"},
    {"name": "Adv. Deepa Krishnan", "specialty": "Family Law", "experience": 14, "rating": 4.7, "cases_won": 230, "phone": "+91 98765 43217", "photo_initials": "DK", "lat": 12.9500, "lng": 77.6300, "city": "Bangalore", "languages": ["English", "Tamil", "Kannada"], "fee": "₹2,500/consultation"},
    {"name": "Adv. Mohammed Fazil", "specialty": "Criminal Law", "experience": 16, "rating": 4.6, "cases_won": 290, "phone": "+91 98765 43218", "photo_initials": "MF", "lat": 13.0200, "lng": 77.5900, "city": "Bangalore", "languages": ["English", "Urdu", "Kannada"], "fee": "₹2,500/consultation"},
    {"name": "Adv. Lakshmi Devi", "specialty": "Civil Law", "experience": 19, "rating": 4.8, "cases_won": 350, "phone": "+91 98765 43219", "photo_initials": "LD", "lat": 12.9300, "lng": 77.5600, "city": "Bangalore", "languages": ["English", "Telugu", "Kannada"], "fee": "₹3,000/consultation"},
    {"name": "Adv. Anand Rao", "specialty": "Property Law", "experience": 21, "rating": 4.7, "cases_won": 410, "phone": "+91 98765 43220", "photo_initials": "AR", "lat": 12.9650, "lng": 77.6000, "city": "Bangalore", "languages": ["English", "Kannada", "Hindi"], "fee": "₹3,000/consultation"},
    {"name": "Adv. Shalini Gupta", "specialty": "Corporate Law", "experience": 13, "rating": 4.9, "cases_won": 200, "phone": "+91 98765 43221", "photo_initials": "SG", "lat": 12.9750, "lng": 77.5750, "city": "Bangalore", "languages": ["English", "Hindi"], "fee": "₹4,000/consultation"},
    {"name": "Adv. Kiran Hegde", "specialty": "Employment Law", "experience": 11, "rating": 4.5, "cases_won": 160, "phone": "+91 98765 43222", "photo_initials": "KH", "lat": 12.9550, "lng": 77.6150, "city": "Bangalore", "languages": ["English", "Kannada", "Tulu"], "fee": "₹2,000/consultation"},
    {"name": "Adv. Ravi Shankar", "specialty": "Criminal Law", "experience": 28, "rating": 4.9, "cases_won": 600, "phone": "+91 98765 43223", "photo_initials": "RK", "lat": 13.0000, "lng": 77.5500, "city": "Bangalore", "languages": ["English", "Hindi", "Kannada"], "fee": "₹5,000/consultation"},
    {"name": "Adv. Sunitha Bhat", "specialty": "Family Law", "experience": 17, "rating": 4.6, "cases_won": 270, "phone": "+91 98765 43224", "photo_initials": "SB", "lat": 12.9450, "lng": 77.5850, "city": "Bangalore", "languages": ["English", "Kannada", "Konkani"], "fee": "₹2,500/consultation"},
]


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def get_recommended_lawyers(specialty, user_lat=None, user_lng=None, limit=5):
    matching = [l for l in LAWYERS if l["specialty"] == specialty]
    if not matching:
        matching = LAWYERS[:]
    for l in matching:
        if user_lat and user_lng:
            l["distance_km"] = round(haversine(user_lat, user_lng, l["lat"], l["lng"]), 1)
        else:
            l["distance_km"] = round(random.uniform(1.5, 12.0), 1)
    matching.sort(key=lambda x: (-x["rating"], x["distance_km"]))
    return matching[:limit]
