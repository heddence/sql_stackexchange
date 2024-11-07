from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Stats(BaseModel):
    """
    Schema representing a percentage of the posts with specific tag each day of the week.

    Attributes:
        day (str): The day of the week of the post.
        percentage (float): Percentage of the posts with specific tag.
    """
    day: str
    percentage: float

    model_config = ConfigDict(from_attributes=True)


class CommentsCount(BaseModel):
    """
    Schema representing the response time statistics between comments on a specific post.

    Attributes:
        post_id (str): The ID of the post.
        comment_seq (int): The sequence number of each comment within the post.
        comment_id (int): The ID of the comment within the post.
        creationdate (datetime): The date the comment was created.
        response_time (float): The response time of the post.
        avg_response_time (float): The average response time of the post.
    """
    post_id: int
    comment_seq: int
    comment_id: int
    creationdate: datetime
    response_time: float
    avg_response_time: float

    model_config = ConfigDict(from_attributes=True)


class CommentsPosLim(BaseModel):
    """
    Schema representing a comment at a specific position within posts that are tagged with a given tag.

    Attributes:
        post_id (int): The unique identifier of the post to which the comment belongs.
        comment_id (int): The unique identifier of the comment.
        creationdate (datetime): The date and time when the comment was created.
        text (str): The content of the comment.
    """
    post_id: int
    comment_id: int
    creationdate: datetime
    text: str

    model_config = ConfigDict(from_attributes=True)
