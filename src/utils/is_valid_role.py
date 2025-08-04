from enum import Enum


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    # Add more roles here in the future, e.g., MODERATOR = "MODERATOR"


def is_valid_role(role: str) -> bool:
    """
    Check if the provided role is valid.

    Args:
        role: The role to validate.

    Returns:
        bool: True if the role is valid, False otherwise.
    """
    return role in Role.__members__
