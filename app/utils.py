import os

from passlib.context import CryptContext
from passlib.hash import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def salt_generator():
    """Generate salt in a form of string of hexadecimal number"""
    return os.urandom(8).hex()


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
