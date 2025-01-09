import os

SECRET_KEY = os.urandom(32).hex()
print(SECRET_KEY)