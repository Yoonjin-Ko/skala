import pytest
from pydantic import ValidationError
from pipeline import WeatherSchema, CountrySchema, IPSchema

def test_weather_success():
    data = WeatherSchema(latitude=37.55, longitude=127.0, temperature=23.2, precipitation_probability=50)
    assert data.latitude == 37.55

def test_temperature_fail():
    with pytest.raises(ValidationError):
        WeatherSchema(latitude=37.55, longitude=127.0, temperature=200, precipitation_probability=50)

def test_country_success():
    data = CountrySchema(name="South Korea", capital="Seoul", population=51780579)
    assert data.name == "South Korea"

def test_ip_success():
    data = IPSchema(country="South Korea", city="Seoul", timezone="Asia/Seoul")
    assert data.country == "South Korea"