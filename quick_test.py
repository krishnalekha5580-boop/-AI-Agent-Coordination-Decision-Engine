from db.session import init_db
from db.repository import create_user, verify_user

init_db()

uid = create_user("krishna", "test1234")
print("Created user with ID:", uid)

result = verify_user("krishna", "test1234")
print("Login with correct password:", result)

result_wrong = verify_user("krishna", "wrongpassword")
print("Login with wrong password:", result_wrong)