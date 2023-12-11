class UserRoleManager:
    def __init__(self):
        self.user_roles = {}

    def set_user_role(self, username, role):
        self.user_roles[username] = role

    def get_user_role(self, username):
        return self.user_roles.get(username, "Guest")

if __name__ == "__main__":
    role_manager = UserRoleManager()
    
    role_manager.set_user_role("SWE", "Admin")
    alice_role = role_manager.get_user_role("SWE")
    assert alice_role == "Admin"
    
    role_manager.set_user_role("NYU", "User")
    bob_role = role_manager.get_user_role("NYU")
    assert bob_role == "User"
