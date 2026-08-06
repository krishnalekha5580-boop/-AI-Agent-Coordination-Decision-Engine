from db.repository import get_project_dates, update_project_dates

# Replace 1 with your actual "E-Commerce Website" project ID
pid = 1

print("Before:", get_project_dates(pid))
update_project_dates(pid, "2026-07-15", "2026-09-01")
print("After:", get_project_dates(pid))