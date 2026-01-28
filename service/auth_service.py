from models.user import User


class AuthService:
    """Business logic for authentication and registration."""

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register(self, username, password):
        """Processes user registration logic."""
        # Check if the user already exists
        if self.user_repository.find_by_username(username):
            return False, "This username is already taken!"

        # Create and save the new user
        new_user = User(username, password)
        self.user_repository.add_user(new_user)
        return True, "Registration successful!"

    def login(self, username, password):
        """Authenticates a user and returns the user object if successful."""
        user = self.user_repository.find_by_username(username)

        if user and user.password == password:
            return user
        return None