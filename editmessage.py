class MessageEditor:
    def __init__(self):
        self.messages = {}

    def send_message(self, user, message):
        self.messages[user] = message

    def edit_message(self, user, edited_message):
        if user in self.messages:
            self.messages[user] = edited_message

    def get_message(self, user):
        return self.messages.get(user, None)


if __name__ == "__main__":
    editor = MessageEditor()
    editor.send_message("SWE", "This is a commit!")

    # Test message editing
    editor.edit_message("SWE", "This is a commit in Python!")
    edited_message = editor.get_message("SWE")
