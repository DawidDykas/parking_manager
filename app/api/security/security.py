"""
Security utilities for password hashing and verification.

Uses passlib with bcrypt backend for secure password hashing.
"""
import asyncio
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


async def hash_password(password: str) -> str:
    """
    Hash a plain-text password asynchronously.

    Uses the configured password context to securely hash the password.
    Execution is offloaded to a separate thread to avoid blocking the event loop.

    Parameters:
    - password (str): Plain-text password

    Returns:
    - str: Hashed password
    """
    return await asyncio.to_thread(pwd_context.hash, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password asynchronously.

    Uses the configured password context to securely verify the password.
    Execution is offloaded to a separate thread to avoid blocking the event loop.

    Parameters:
    - plain_password (str): Plain-text password
    - hashed_password (str): Hashed password to verify against

    Returns:
    - bool: True if the password matches, False otherwise
    """
    return await asyncio.to_thread(pwd_context.verify, plain_password, hashed_password)
