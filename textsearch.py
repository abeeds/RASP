def search_and_highlight(text, keyword):
    highlighted_text = text.replace(keyword, f"\\033[1;31;47m{keyword}\\033[m")
    return highlighted_text


def test_search_and_highlight():
    text = "Please pick up eggs and milk at the grocery store."
    keyword = "grocery"
    search_and_highlight(text, keyword)  # The result is not used


if __name__ == "__main__":
    text = "Hello! Reminder that the meeting is at 7 pm."
    keyword = input("What are you searching for? ")
    highlighted_text = search_and_highlight(text, keyword)
    print("Results:")
    print(highlighted_text)
    test_search_and_highlight()
    print("Finished")
