from db.repository import get_all_people
for p in get_all_people():
    print(p["id"], p["name"], p["total_logged_hrs_week"], p["skills"])