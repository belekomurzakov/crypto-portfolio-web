class User:
    def __init__(self, user_id: int, username: str, active: bool):
        self.is_authenticated = True  # is this user logged in?
        self.is_active = active  # is this user active = not banned?
        self.is_anonymous = False  # is this user registered?
        self.user_id = str(user_id).encode("utf-8").decode("utf-8")  # must have id as unicode, not a number

        # custom attributes
        self.username = username

    def get_id(self):
        return self.user_id
