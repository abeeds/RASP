user_contacts = {
    "johnny215": ["rosa413", "chance338"],
    "rosa413": ["johnny215", "chance338"],
    "chance338": ["johnny215", "rosa413"],
}

def display_contacts(username):
    if username in user_contacts:
        contacts = user_contacts[username]
        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print(f"{username} has no friends.")
    else:
        print("No profile match.")

def add_contact(username, new_contact):
    if username in user_contacts:
        if new_contact not in user_contacts[username]:
            user_contacts[username].append(new_contact)
            print(f"{new_contact} has been added to {username}'s friend list!.")
        else:
            print(f"{new_contact} is already in {username}'s friend list!.")
    else:
        print("No profile match.")

if __name__ == "__main__":
    while True:
        choice = input("Would you like to view your friends, add a new friend or exit?").strip().lower()
        
        if choice == "view" or choice == "View":
            username = input("Please enter username: ")
            display_contacts(username)
        elif choice == "add" or choice == "Add":
            username = input("Please enter your username: ")
            new_contact = input("Please enter the friend username: ")
            add_contact(username, new_contact)
        elif choice == "exit" or choice == "Exit":
            print("Logging Off")
            break
        else:
            print("Error. Try again.")