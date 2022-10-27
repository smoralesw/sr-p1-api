from sqlalchemy import and_
from sqlalchemy.orm import Session
from models import Track
from schemas import TrackSchema


def getTrack(db: Session, track: str, artist: str):
    return db.query(Track).filter(and_(Track.track_name == track, Track.artist_name == artist)).first()

def get_track_by_id(db: Session, track_id: int):
    return db.query(Track).filter(Track.id == track_id).first()

def create_track(db: Session, track: TrackSchema):
    db_track = Track(track_uri=track.track_uri,
                     track_name=track.track_name,
                     artist_name=track.artist_name)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track