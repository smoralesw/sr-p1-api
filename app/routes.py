from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import Response, RequestTrack, RequestTrack_

import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HOME
@router.get("/")
async def home():
    return ("HOME")

# GET TRACKS BY ID
@router.get("/addTrackSpotify/{id}")
async def get_by_id(id: str, db: Session = Depends(get_db)):
    # Send track id to spotify api and update favorites
    return crud.add_track_spotify(db, id)

# GET TRACKS BY NAME & ARTIST
@router.post("/getPath")
async def getTracks(request: RequestTrack, db: Session = Depends(get_db)):
    print(1)
    trackIn = crud.getTrack(db, track=request.nameIn, artist=request.artistIn)
    print(2)
    trackOut = crud.getTrack(db, track=request.nameOut, artist=request.artistOut)
    print(3)
    genre = request.genre

    most_stable = crud.getPath(trackIn.id, trackOut.id, genre)
    print(4)
    ms_tracks = crud.get_names_from_path(db, most_stable)
    print(5)
    status = "OK"
    code = "200"
    msg = "Paths Discovered Successfully"

    if (most_stable == None):
        status = "ERROR"
        code = "404"
        msg = "Couldn't get paths"

    return Response(status=status,
                    code=code,
                    message=msg,
                    result={"most_stable_paths": ms_tracks}).dict(exclude_none=True)

@router.post("/getTracks")
async def getTracks(request: RequestTrack, db: Session = Depends(get_db)):
    print(request.artistIn)
    print(request.trackIn)
    
    trackIn = crud.getTrack(db, track=request.nameIn, artist=request.artistIn)
    trackOut = crud.getTrack(db, track=request.nameOut, artist=request.artistOut)
    
    status = "OK"
    code = "200"
    msg = "Tracks Found Successfully"

    if (trackIn == None) or (trackOut == None):
        status = "ERROR"
        code = "404"
        msg = "At Least One Track Not Found"

    return Response(status=status,
                    code=code,
                    message=msg,
                    result={"trackIn": trackIn, "trackOut": trackOut}).dict(exclude_none=True)


# CREATE TRACK
@router.post("/create")
async def createTrack(request: RequestTrack_, db: Session = Depends(get_db)):
    crud.create_track(db, track=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Track created successfully").dict(exclude_none=True)
