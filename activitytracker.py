class UserActivityTracker:
    def __init__(self):
        self.user_activity = {}

    def track_activity(self, username, activity):
        if username not in self.user_activity:
            self.user_activity[username] = []
        self.user_activity[username].append(activity)

    def get_user_activity(self, username):
        return self.user_activity.get(username, [])

if __name__ == "__main__":
    activity_tracker = UserActivityTracker()
    
    activity_tracker.track_activity("SWE", "Logged in")
    alice_activity = activity_tracker.get_user_activity("SWE")
    assert alice_activity == ["Logged in"]
    
    activity_tracker.track_activity("NYU", "Sent a message")
    bob_activity = activity_tracker.get_user_activity("NYU")
    assert bob_activity == ["Sent a message"]
