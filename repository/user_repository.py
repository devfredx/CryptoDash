class UserRepository:
    """Handles data operations for User objects."""

    def __init__(self):
        # In-memory list to store users for now
        self.users = []

    def add_user(self, user):
        """Adds a new user to the repository."""
        self.users.append(user)

    def find_by_username(self, username):
        """Returns a user object if found, otherwise None."""
        for user in self.users:
            if user.username == username:
                return user
        return None