import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from ..src.modules.events.event import get_events, create_event

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.query.return_value.all.return_value = [
        MagicMock(name="Event1"), MagicMock(name="Event2")
    ]
    db.execute.return_value = None
    db.commit.return_value = None
    return db

def test_get_events_success(mock_db):
    result = get_events(mock_db)
    assert "events" in result
    assert isinstance(result["events"], list)

def test_get_events_exception():
    db = MagicMock()
    db.query.side_effect = Exception("DB error")
    with pytest.raises(HTTPException) as excinfo:
        get_events(db)
    assert excinfo.value.status_code == 500
    assert "DB error" in str(excinfo.value.detail)

@pytest.fixture
def event_details():
    details = MagicMock()
    details.dict.return_value = {
        "name": "Test Event",
        "location": "Test Location",
        "start_time": "2024-06-12T10:00:00",
        "end_time": "2024-06-12T12:00:00",
        "max_capacity": 100
    }
    return details

def test_create_event_success(event_details, mock_db):
    result = create_event(event_details, mock_db)
    assert result["message"] == "Event Created successfully"

def test_create_event_integrity_error(event_details):
    db = MagicMock()
    db.execute.side_effect = Exception("IntegrityError")
    with pytest.raises(HTTPException) as excinfo:
        create_event(event_details, db)
    assert excinfo.value.status_code == 500
    assert "IntegrityError" in str(excinfo.value.detail)