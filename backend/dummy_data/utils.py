from dummy_data.models import CustomUser

def authenticate(email=None, password=None):
    """
    Authenticate a user based on email and password.

    This function retrieves a `CustomUser` instance by email and checks if
    the provided password matches the stored password for that user. If
    the user exists and the password is correct, the user instance is returned.
    Otherwise, `None` is returned.

    Args:
        email (str, optional): The email address of the user to authenticate.
        password (str, optional): The password of the user to authenticate.

    Returns:
        CustomUser or None: Returns the `CustomUser` instance if the email and
        password are valid; otherwise, returns `None`.

    Raises:
        CustomUser.DoesNotExist: If no user with the provided email exists,
        a `CustomUser.DoesNotExist` exception is caught and handled by returning `None`.
    """
    try:
        user = CustomUser.objects.get(email=email)
        if user.check_password(password):
            return user
    except CustomUser.DoesNotExist:
        return None
