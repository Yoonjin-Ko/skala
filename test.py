import pytest
from pydantic import ValidationError

from pipeline import WeatherSchema


# 정상 데이터 테스트
def test_weather_success():

    data = WeatherSchema(
        latitude=37.55,
        longitude=127.0,
        temperature=23.2,
        precipitation_probability=50
    )

    assert data.latitude == 37.55
    assert data.temperature == 23.2


# 경계값(정확히 min/max)도 통과해야 함
def test_weather_boundary_values_pass():

    data = WeatherSchema(
        latitude=90,
        longitude=180,
        temperature=60,
        precipitation_probability=100
    )

    assert data.temperature == 60
    assert data.precipitation_probability == 100


# 온도 범위 오류 테스트 (상한 초과)
def test_temperature_fail_upper():

    with pytest.raises(ValidationError):

        WeatherSchema(
            latitude=37.55,
            longitude=127.0,
            temperature=200,
            precipitation_probability=50
        )


# 온도 범위 오류 테스트 (하한 미만)
def test_temperature_fail_lower():

    with pytest.raises(ValidationError):

        WeatherSchema(
            latitude=37.55,
            longitude=127.0,
            temperature=-150,
            precipitation_probability=50
        )


# 강수확률 범위 오류 테스트
def test_probability_fail():

    with pytest.raises(ValidationError):

        WeatherSchema(
            latitude=37.55,
            longitude=127.0,
            temperature=20,
            precipitation_probability=150
        )


# 위도 범위 오류 테스트
def test_latitude_fail():

    with pytest.raises(ValidationError):

        WeatherSchema(
            latitude=91,
            longitude=127.0,
            temperature=20,
            precipitation_probability=50
        )