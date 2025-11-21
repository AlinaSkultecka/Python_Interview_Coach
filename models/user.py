class User:
    """
    Simple model representing an app user.
    Currently stores only a username.
    """

    def __init__(self, username="user"):
        self.username = username