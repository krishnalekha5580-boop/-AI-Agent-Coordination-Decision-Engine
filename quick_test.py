from db.repository import create_project, add_task, get_last_data_change, update_task, get_tasks_with_db_id
import time

pid = create_project("Stale Data Test", "2026-08-01", "2026-09-01")
print("Created project ID:", pid)

add_task(pid, "T1", "Sample Task", 20, "2026-08-20", [], "TestPerson")
print("Task added")

print("Last data change right after adding:", get_last_data_change(pid))

time.sleep(2)  # small pause so the 'before' and 'after' timestamps are clearly different

tasks = get_tasks_with_db_id(pid)
t = tasks[0]
update_task(t["db_id"], "Updated Task Name", 55, t["planned_end"], t["depends_on"], t["assigned_to"])
print("Task updated")

print("Last data change after edit:", get_last_data_change(pid))