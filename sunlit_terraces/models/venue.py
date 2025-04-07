from pydantic import BaseModel


class Venue(BaseModel):
    name: str
    latitude: float
    longitude: float
    rating: float
