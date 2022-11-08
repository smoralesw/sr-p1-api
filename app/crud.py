from sqlalchemy import and_
from sqlalchemy.orm import Session
from models import Track
from schemas import TrackSchema
import paths
import networkx as nx
from networkx.readwrite import json_graph

def get_names_from_path(db: Session, stable_paths: dict):
    paths = dict()
    for path_len, nodes in stable_paths.items():
        ms_path = list()
        for n in nodes[0]:
            track = db.query(Track).filter(Track.id == n).first()
            ms_path.append(track.track_name + "  ---  " + track.artist_name)
        paths[path_len] = ms_path
    return paths

def getPath(id_1, id_2):
    G = nx.read_gpickle("hardrockslimmer.gpickle")
    most_stable, all_stable_paths = paths.most_stable_paths(G, id_1, id_2)



    return most_stable

def getTrack(db: Session, track: str, artist: str):
    track = db.query(Track).filter(and_(Track.track_name.ilike('%' + track + '%'), Track.artist_name.ilike('%' + artist + '%'))).first()
    return track

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