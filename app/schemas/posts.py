from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


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


class DurationLimit(BaseModel):
    """"
    Schema representing a recently resolved post with its duration of being open.

    Attributes:
        id (int): The unique identifier of the post.
        title (str): The title of the post.
        creationdate (datetime): The timestamp when the post was created.
        closeddate (datetime): The timestamp when the post was closed.
        duration (float): The duration in minutes the post was open, rounded to two decimal places.
    """
    id: int
    title: str
    creationdate: datetime
    closeddate: datetime
    duration: float

    model_config = ConfigDict(from_attributes=True)


class LimitQuery(BaseModel):
    """
    Schema representing a post with associated tags.

    Attributes:
        id (int): The unique identifier of the post.
        title (str): The title of the post.
        creationdate (datetime): The timestamp when the post was created.
        body (str): The content of the post.
        tags (List[str]): A list of associated tags for the post.
    """
    id: int
    title: str
    creationdate: datetime
    body: str
    tags: List[str] = Field(default_factory=list, description="Associated tags")

    model_config = ConfigDict(from_attributes=True)
