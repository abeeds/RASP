import os
import shutil
PROFILE_PICS_DIR = "profile_pics"

def upload_profile_photo(username):
    user_profile_dir = os.path.join(PROFILE_PICS_DIR, username)
    os.makedirs(user_profile_dir, exist_ok=True)
    uploaded_image = input("Upload your profile photo: ")
    if os.path.exists(uploaded_image):
        destination = os.path.join(user_profile_dir, "profile.png")
        shutil.copy(uploaded_image, destination)
        print("Congrats on your new photo!")
    else:
        print("File is incompatible")

if __name__ == "__main__":
    while True:
        choice = input("Would you like to upload a profile photo?").strip().lower()
        if choice == "yes" or choice == "Yes":
            username = input("Enter your username: ")
            upload_profile_photo(username)
        elif choice == "no" or choice == "No":
            break
        else:
            print("Error. Try again.")