from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Friends(BaseModel):
    """
    Schema representing a friend user who has interacted with the specified user's posts.

    Attributes:
        user_id (int): The unique identifier of the friend user.
        display_name (str): The display name of the friend user.
        reputation (int): The reputation score of the friend user.
        last_comment_date (datetime): The most recent comment date by the friend user on relevant posts.
    """
    user_id: int
    display_name: str
    reputation: int
    last_comment_date: datetime

    model_config = ConfigDict(from_attributes=True)


class IdBadgeHistory(BaseModel):
    """"
    Schema representing the badge history for a user, including the badge earned,
    the associated post made before earning the badge, and details of that post.

    Attributes:
        badge_name (str): The name of the badge.
        post_id (int): The unique identifier of the post made before earning the badge.
        post_date (datetime): The date and time when the post was created.
        post_body (str): The content of the post made before earning the badge.
    """
    badge_name: str
    post_id: int
    post_date: datetime
    post_body: str

    model_config = ConfigDict(from_attributes=True)
