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
