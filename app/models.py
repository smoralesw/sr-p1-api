from sqlalchemy import  Column, Integer, String
from config import Base
class Track(Base):
    __tablename__ ="tracks"

    id = Column(Integer, primary_key=True, index=True)
    track_uri = Column(String)
    track_name = Column(String)
    artist_name = Column(String)
    genres = Column(String)
