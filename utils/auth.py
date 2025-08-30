def login_user(username: str, password: str) -> bool:
    """
    Simulates a user login process.

    In a real application, this would involve hashing the password and
    checking against a database of users. For this demo, we'll use
    hardcoded credentials.

    Args:
        username (str): The user's entered username.
        password (str): The user's entered password.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    # Simple validation: checks if username and password are not empty
    # and match our "database"
    if not username or not password:
        return False

    # Dummy users for demonstration
    valid_users = {
        "student": "pass123",
        "professional": "pass456"
    }

    return username in valid_users and valid_users[username] == password
