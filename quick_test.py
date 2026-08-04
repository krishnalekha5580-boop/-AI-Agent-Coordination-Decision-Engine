from db.session import init_db
from db.repository import (
    create_project, add_task, get_tasks_with_db_id,
    update_task, delete_task
)

init_db()

pid = create_project("Edit Delete Test")
add_task(pid, "T1", "Test Task", 20, "2026-09-01", [], "TestPerson")

print("Before update:")
print(get_tasks_with_db_id(pid))

tasks = get_tasks_with_db_id(pid)
db_id = tasks[0]["db_id"]
update_task(db_id, "Updated Task Name", 55, "2026-09-15", [], "TestPerson")

print("\nAfter update:")
print(get_tasks_with_db_id(pid))

delete_task(db_id)

print("\nAfter delete:")
print(get_tasks_with_db_id(pid))