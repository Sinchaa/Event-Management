from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..modules.events.schema import CreateEventRequest
from ..modules.register_event.validate_schema import CreateAttendeeRequest

from ..modules.events.event import get_events, create_event
from ..modules.register_event.register_event import add_attendee, get_attendees

router = APIRouter(prefix='/events')

@router.get("")
async def fetch_all_events(db: Session = Depends(get_db)):
    return get_events(db)
     

@router.post("")
async def add_event(event_details: CreateEventRequest, db: Session = Depends(get_db)):
    return create_event(event_details,  db)

@router.post("/{event_id}/register")
async def register_attendee(event_id: int | None, attendee_details: CreateAttendeeRequest, db: Session = Depends(get_db)):
    return add_attendee(event_id, attendee_details, db)

@router.get("/{event_id}/attendees")
async def fetch_all_events(event_id: int | None,offset: int = 0, limit: int = 10,db: Session = Depends(get_db)):
    return get_attendees(event_id, db,offset, limit)
