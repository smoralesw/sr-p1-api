from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import Request, Response, RequestTrack

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
@router.get("/{id}")
async def get_by_id(id: int, db: Session = Depends(get_db)):
    track = crud.get_track_by_id(db, id)
    status = "OK"
    code = "200"
    msg = "Track found"
    if (track == None):
        msg = "Track not found"
        status = "ERROR"
        code = "404"

    return Response(status=status, code=code, message=msg, result=track)

# GET TRACKS BY NAME & ARTIST
@router.post("/getTracks")
async def getTracks(request: RequestTrack, db: Session = Depends(get_db)):
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
async def createTrack(request: RequestTrack, db: Session = Depends(get_db)):
    crud.create_track(db, track=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Track created successfully").dict(exclude_none=True)
