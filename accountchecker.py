import csv

def login_user():
    username = input("Username: ")
    password = input("Password: ")
    if check_credentials(username, password):
        print("Login successful.")
    else:
        print("Invalid username or password. Please try again.")

#Will implement dictionary for all account usernames and passwords
def check_credentials(username, password):
    with open("users.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

if __name__ == "__main__":
    print("Welcome!")
    while True:
        choice = input("Do you have an account?").strip().lower()
        if choice == "yes":
            login_user()
        elif choice == "no":
            print("TBD, will reference account creation")
            break
        else:
            print("Unable to process request")
