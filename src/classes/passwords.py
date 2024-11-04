import bcrypt


"""
Guide for storing Passwords
https://www.askpython.com/python/examples/storing-retrieving-passwords-securely
"""


class Password:
    def __init__(self):
        pass

    def create_secure_password(self, password: str):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=password.encode(), salt=salt)
        return hashed_password

    def verify_password(self, password: str, hashed_password: str):
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password.encode()
        )
