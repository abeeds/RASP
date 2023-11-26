class Database:
    def __init__(self):
        self.data = {}

    def store_data(self, key, value):
        self.data[key] = value

    def retrieve_data(self, key):
        return self.data.get(key, None)

    def delete_data(self, key):
        if key in self.data:
            del self.data[key]


if __name__ == "__main__":
    db = Database()

    db.store_data("rasp", {"name": "SWE", "email": "swe@nyu.edu"})

    user_data = db.retrieve_data("rasp")
    print("Retrieved User Data:", user_data)

    db.delete_data("rasp")
    deleted_data = db.retrieve_data("rasp")
    print("Deleted User Data:", deleted_data)
