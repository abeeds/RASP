import random

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
    return username in user_data and user_data[username] == password


def enable_2fa(username):
    if username in user_data:
        two_factor_auth[username] = True
        print("Two-Factor Authentication enabled")
    else:
        print("Error")


def generate_2fa_code(username):
    two_factor_codes[username] = str(random.randint(1000, 9999))


def perform_2fa(username):
    if username in user_data and two_factor_auth.get(username, False):
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

    assert verify_login(username, new_password), "Password reset failed"


if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    if verify_login(username, password):
        reset_choice = input("Forgot your password?").lower()
        if reset_choice == "yes":
            if perform_2fa(username):
                new_password = input("New password: ")
                reset_password(username, new_password)
    else:
        print("Login Error")
    test_reset_password()
    print("Finished")
