import pytest
from unittest.mock import MagicMock
from ..src.modules.register_event.register_event import get_attendees

@pytest.fixture
def mock_db_attendees():
    db = MagicMock()
    alice = MagicMock()
    alice.name = "Alice"
    alice.email = "alice@example.com"
    bob = MagicMock()
    bob.name = "Bob"
    bob.email = "bob@example.com"
    attendee_rows = [alice, bob]
    db.execute.return_value.all.return_value = attendee_rows
    return db

def test_get_attendees_success(mock_db_attendees):
    event_id = 1
    offset = 0
    limit = 1
    result = get_attendees(event_id, mock_db_attendees, offset, limit)
    assert "attendees" in result
    assert len(result["attendees"]) == 2
    assert result["attendees"][0]["name"] == "Alice"
    assert result["attendees"][1]["email"] == "bob@example.com"

from fastapi import HTTPException
from ..src.modules.register_event.register_event import add_attendee

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.execute.return_value.all.return_value = []
    db.execute.return_value.fetchone.return_value = [2]
    return db

@pytest.fixture
def attendee_details():
    details = MagicMock()
    details.dict.return_value = {"name": "Alice", "email": "alice@example.com"}
    return details

def test_add_attendee_success(mock_db, attendee_details):
    def execute_side_effect(query):
        if "attendees" in str(query):
            if "email" in str(query):
                mock = MagicMock()
                mock.all.return_value = []
                return mock
            mock = MagicMock()
            mock.all.return_value = [{}]
            return mock
        if "max_capacity" in str(query):
            mock = MagicMock()
            mock.fetchone.return_value = [2]
            return mock
        return MagicMock()
    mock_db.execute.side_effect = execute_side_effect

    result = add_attendee(1, attendee_details, mock_db)
    assert result["message"] == "Attendee added successfully"

def test_add_attendee_already_registered(mock_db, attendee_details):
    def execute_side_effect(query):
        if "attendees" in str(query) and "email" in str(query):
            mock = MagicMock()
            mock.all.return_value = [{}]
            return mock
        if "max_capacity" in str(query):
            mock = MagicMock()
            mock.fetchone.return_value = [2]
            return mock
        mock = MagicMock()
        mock.all.return_value = []
        return mock
    mock_db.execute.side_effect = execute_side_effect

    with pytest.raises(HTTPException) as excinfo:
        add_attendee(1, attendee_details, mock_db)
    assert "Attendee already registered" in str(excinfo.value.detail)

def test_add_attendee_capacity_exceeded(mock_db, attendee_details):
    call_results = [
        MagicMock(all=MagicMock(return_value=[])),
        MagicMock(fetchone=MagicMock(return_value=[1])),
        MagicMock(all=MagicMock(return_value=[{}])),
    ]
    mock_db.execute.side_effect = call_results

    with pytest.raises(HTTPException) as excinfo:
        add_attendee(1, attendee_details, mock_db)
    assert "Number of Attendee exceeded" in str(excinfo.value.detail)