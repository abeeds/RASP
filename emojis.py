import emoji

emoji_dict = {
    "thumbs_up": ":thumbsup:",
    "heart_eyes": ":heart_eyes:",
    "smile": ":smile:",
    "fire": ":fire:",
    "rocket": ":rocket:",
}


def send_message_with_emoji(sender, receiver, message):
    formatted_message = message
    for alias, emoji_code in emoji_dict.items():
        formatted_message = formatted_message.replace(
            alias, emoji.emojize(emoji_code, use_aliases=True))
    print(f"{sender}: {formatted_message}")
    return formatted_message


def test_send_message_with_emoji():
    sender = "NYU"
    receiver = "Tandon"
    message = "You are :heart_eyes: and :fire: :thumbs_up: :rocket:"
    expected_message = "You are 😍 and 🔥 👍 🚀"

    result = send_message_with_emoji(sender, receiver, message)
    assert result == expected_message, (
        f"Expected: {expected_message}, "
        f"but got: {result}"
    )


if __name__ == "__main__":
    sender = input("Username: ")
    receiver = input("Recipient: ")
    message = input("Your text here: ")
    formatted_message = send_message_with_emoji(sender, receiver, message)
    print(formatted_message)

    test_send_message_with_emoji()
