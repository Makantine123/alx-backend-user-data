#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

new_user = auth.register_user(email, password)
print(f"Registered users: {new_user.email} and hash: {new_user.hashed_password}")
print("+---------------------------------------------+")
print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))
