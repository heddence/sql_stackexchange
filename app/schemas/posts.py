from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Users(BaseModel):
    """
    Schema representing a discussant (user) who has commented on a specific post.

    Attributes:
        user_id (int): The unique identifier for the user.
        display_name (str): The display name of the user.
        reputation (int): The reputation score of the user.
        last_comment_date (datetime): The date and time of the user's most recent comment on the post.
    """
    user_id: int
    display_name: str
    reputation: int
    last_comment_date: datetime

    model_config = ConfigDict(from_attributes=True)
