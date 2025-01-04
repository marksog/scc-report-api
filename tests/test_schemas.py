import pytest
from marshmallow import ValidationError
from app.schemas import PrayerSchema

def test_prayer_schema_validation():
    schema = PrayerSchema()
    # invalid times: start >= end
    invalid_data = {
        "prayer_chain_start": "10:00:00",
        "prayer_chain_end": "09:59:59"
    }
    with pytest.raises(ValidationError):
        schema.load(invalid_data)