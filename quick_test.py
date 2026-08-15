from db.repository import get_tasks, get_team_members

pid = 6
tasks = get_tasks(pid)
team = get_team_members(pid)

print("Tasks and assignees:")
for t in tasks:
    print(" ", t["id"], "-", t["name"], "-> assigned to:", repr(t["assigned_to"]))

print("\nTeam members actually in project:")
for m in team:
    print(" ", repr(m["name"]))