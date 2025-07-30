from fastapi import HTTPException 
from sqlalchemy import update

from sqlalchemy.exc import IntegrityError

#models
from .models import Event


def get_events(db):
    try:
        print(f'Fetching all the events')
        events = db.query(Event).all()
        return {"events": events}
    except Exception as e:
      print(f'Something went wrong while fetching :{e}')
      raise HTTPException(status_code=500, detail=str(e))    
    

def create_event(event_details, db):
    try:
        print(f'Creating new event with details: {event_details}')
        event_details = event_details.dict()
        # new_event = Event(event_details)
        # db.add(new_event)
        db.execute(Event.__table__.insert().values(event_details))
        db.commit()
        print('Event created successfully')
        return {
            'message':'Event Created successfully'
        }
    except IntegrityError as e:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f'Something went wrong while creating new event :{e}')
        raise HTTPException(status_code=500, detail=str(e))

    