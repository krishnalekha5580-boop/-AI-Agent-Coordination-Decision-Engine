from db.session import init_db
from db.repository import create_project, add_team_member, get_team_members

init_db()

pid1 = create_project("Clean Test A")
pid2 = create_project("Clean Test B")

add_team_member(pid1, "Fresh Person", 40, 30, ["Testing"])
add_team_member(pid2, "Fresh Person", 40, 20, ["Testing"])

print("Project A:", get_team_members(pid1))
print("Project B:", get_team_members(pid2))