from fastapi import HTTPException 
from sqlalchemy import select

#models
from .models import Attendee
from ..events.models import Event


def add_attendee(event_id, attendee_details, db):
    try:
        print(f'Creating new attendee for event_id: {event_id},{attendee_details}')
        attendee_details = attendee_details.dict()
        if len(db.execute(select(Attendee).where(Attendee.event_id == event_id,Attendee.email == attendee_details['email'])).all()):
            raise Exception('Attendee already registered')
        
        # check the max_Capacity
        capacity = db.execute(select(Event.max_capacity).where(Event.event_id == event_id)).fetchone()[0]

        attendees_count = len(db.execute(select(Attendee).where(Attendee.event_id == event_id)).all())
        if attendees_count +1 > capacity:
            raise Exception('Number of Attendee exceeded')
        
        attendee_details['event_id'] = event_id
        
        db.execute(Attendee.__table__.insert().values(attendee_details))
        db.commit()
        print("Inserted the attendee successfully")
        return {
            'message':'Attendee added successfully'
        }
    except Exception as e:
      print(f'Something went wrong while fetching :{e}')
      raise HTTPException(status_code=500, detail=str(e))    
    

def get_attendees(event_id,db, offset: int = 0, limit: int = 10):
    try:
        print(f'Fetching all the attendees for event_id: {event_id}, offset: {offset}, limit: {limit}')
        result = db.execute(select(Attendee.name, Attendee.email).where(Attendee.event_id == event_id).offset(offset)
            .limit(limit)).all()
        attendees = [{"name": row.name, "email": row.email} for row in result]
        return {"attendees": attendees}
    except Exception as e:
      print(f'Something went wrong while fetching :{e}')
      raise HTTPException(status_code=500, detail=str(e))    