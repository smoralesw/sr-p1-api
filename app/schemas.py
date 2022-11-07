from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class TrackSchema(BaseModel):
    id: Optional[int] = None
    track_uri: Optional[str] = None
    track_name: Optional[str] = None
    artist_name: Optional[str] = None
    genres: Optional[str] = None

    class Config:
        orm_mode = True

class RequestTrack(BaseModel):
    nameIn: str
    artistIn: str
    nameOut: str
    artistOut: str

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)

class RequestTrack_(BaseModel):
    parameter: TrackSchema = Field(...)

class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]