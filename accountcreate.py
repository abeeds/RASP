import csv


def register_user():
    username = input("Username: ")
    password = input("Password: ")

    if username_exists(username):
        print("Username already taken.")
        return

    with open("users.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
        print("Account created.")


def username_exists(username):
    with open("users.csv", mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return True
    return False


if __name__ == "__main__":
    print("Sign Up!")
    while True:
        choice = input("Would you like to sign up?").strip().lower()
        if choice == "yes":
            register_user()
        elif choice == "no":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")
