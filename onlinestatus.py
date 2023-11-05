user_status = {}

def set_online_status(username, is_online=True):
    user_status[username] = is_online

def get_online_status(username):
    return user_status.get(username, False)

def log_out(username):
    set_online_status(username, False)

def display_user_status(username):
    status = "Online" if get_online_status(username) else "Offline"
    print(f"{username} is {status}")

def test_user_status():
    username = "NYU"
    
    set_online_status(username, True)
    assert get_online_status(username) == True, "Expected online status to be True, but got False"
    
    log_out(username)
    assert get_online_status(username) == False, "Expected online status to be False, but got True"

if __name__ == "__main__":
    username = input("Username: ")
    
    set_online_status(username, True)
    display_user_status(username)
    
    log_out_choice = input("Do you want to log out?").lower()
    if log_out_choice == "yes":
        log_out(username)
        display_user_status(username)
    
    test_user_status()
    print("Test passed.")
