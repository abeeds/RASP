user_data = {}
two_factor_auth = {}
two_factor_codes = {}

def reset_password(username, new_password):
    if username in user_data:
        user_data[username] = new_password
        print("Password reset")
    else:
        print("Unable to find user")

def verify_login(username, password):
    if username in user_data and user_data[username] == password:
        return True
    return False
    
def enable_2fa(username):
    if username in user_data:
        two_factor_auth[username] = True
        print(f"Two-Factor Authentication enabled")
    else:
        print("Error")
        
def generate_2fa_code(username):
    import random
    two_factor_codes[username] = str(random.randint(1000, 9999))

def perform_2fa(username):
    if username in user_data and username in two_factor_auth and two_factor_auth[username]:
        phone_number = user_data[username]["phone_number"]
        #the function will simulate sending a code to a phone number
        #i will figure out how to do this more later
        generate_2fa_code(username)
        input_code = input("Code: ")
        stored_code = two_factor_codes.get(username, "")
        
        if input_code == stored_code:
            print("Authentication Complete")
            return True
        else:
            print("Incorrect Code")
    
    return False

def test_reset_password():
    username = "swe123"
    old_password = "password"
    new_password = "Betterpassword456!"
    
    user_data[username] = old_password
    reset_password(username, new_password)
    
    assert verify_login(username, new_password) == True, "Password reset failed"

if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    if verify_login(username, password):
        #i know this line doesn't make sense after already entering your
        #password but the above were for test purposes
        reset_choice = input("Forgot your password?").lower()
        if reset_choice == "yes":
            if perform_2fa(username):
                new_password = input("New password: ")
                reset_password(username, new_password)
    else:
        print("Login Error")
    test_reset_password()
    print("Finished")
