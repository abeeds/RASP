class MessageDeleter:
    def __init__(self):
        self.messages = {}

    def send_message(self, user, message):
        self.messages[user] = message

    def delete_message(self, user):
        if user in self.messages:
            del self.messages[user]

    def get_message(self, user):
        return self.messages.get(user, None)


if __name__ == "__main__":
    deleter = MessageDeleter()
    deleter.send_message("SWE", "This is a commit!")

    # Test message deletion
    deleter.delete_message("SWE")
    deleted_message = deleter.get_message("SWE")
