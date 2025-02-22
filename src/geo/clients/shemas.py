"""
Описание моделей данных (DTO).
"""
from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel

from base.clients.shemas import HashableBaseModel


class LocationDTO(HashableBaseModel):
    """
    Модель локации для получения сведений о погоде.

    .. code-block::

        LocationDTO(
            city="Mariehamn",
            alpha2code="AX",
        )
    """

    city: str
    alpha2code: str = Field(min_length=2, max_length=2)  # country alpha‑2 code


class CurrencyInfoDTO(HashableBaseModel):
    """
    Модель данных о валюте.

    .. code-block::

        CurrencyInfoDTO(
            code="EUR",
        )
    """

    code: str


class LanguagesInfoDTO(HashableBaseModel):
    """
    Модель данных о языке.

    .. code-block::

        LanguagesInfoDTO(
            name="Swedish",
            native_name="svenska"
        )
    """

    name: str
    native_name: str


class CountryShortDTO(BaseModel):
    """
    Модель базовых данных о стране.

    .. code-block::

        CountryShortDTO(
            name=\u00c5land Islands",
            alpha2code="AX",
        )
    """

    name: str
    alpha2code: str


class CountryDTO(CountryShortDTO):
    """
    Модель данных о стране.

    .. code-block::

        CountryDTO(
            capital="Mariehamn",
            alpha2code="AX",
            alt_spellings=[
              "AX",
              "Aaland",
              "Aland",
              "Ahvenanmaa"
            ],
            currencies={
                CurrencyInfoDTO(
                    code="EUR",
                )
            },
            flag="http://assets.promptapi.com/flags/AX.svg",
            languages={
                LanguagesInfoDTO(
                    name="Swedish",
                    native_name="svenska"
                )
            },
            name="\u00c5land Islands",
            population=28875,
            subregion="Northern Europe",
            timezones=[
                "UTC+02:00",
            ],
        )
    """

    alpha3code: str
    capital: str
    region: str
    subregion: str
    population: int
    latitude: float
    longitude: float
    demonym: str
    area: float
    numeric_code: str
    flag: str
    currencies: set[CurrencyInfoDTO]
    languages: set[LanguagesInfoDTO]


class CityDTO(BaseModel):
    """
    Модель данных о городе.

    .. code-block::

        CityDTO(
            name="Tallinn",
            state_or_region="Harjumaa",
            country=CountryShortDTO(
                name="Estonia",
                alpha2code="EE",
            ),
            latitude=59.436958,
            longitude=24.753531,
        )
    """

    name: str
    state_or_region: Optional[str]
    country: CountryShortDTO
    latitude: float
    longitude: float


class CurrencyRatesDTO(BaseModel):
    """
    Модель данных о курсах валют.

    .. code-block::

        CurrencyRatesDTO(
            base="RUB",
            date="2022-09-14",
            rates={
                "EUR": 0.016503,
            }
        )
    """

    base: str
    date: str
    rates: dict[str, float]


class WeatherInfoDTO(BaseModel):
    """
    Модель данных о погоде.

    .. code-block::

        WeatherInfoDTO(
            temp=13.92,
            pressure=1023,
            humidity=54,
            wind_speed=4.63,
            description="scattered clouds",
            visibility=10000,
            dt=1661870592,
            timezone=7200,
        )
    """

    temp: float
    pressure: int
    humidity: int
    wind_speed: float
    description: str
    visibility: int
    dt: datetime
    timezone: int


class LocationInfoDTO(BaseModel):
    """
    Модель данных для представления общей информации о месте.

    .. code-block::

        LocationInfoDTO(
            location=CountryDTO(
                capital="Mariehamn",
                alpha2code="AX",
                alt_spellings=[
                  "AX",
                  "Aaland",
                  "Aland",
                  "Ahvenanmaa"
                ],
                currencies={
                    CurrencyInfoDTO(
                        code="EUR",
                    )
                },
                flag="http://assets.promptapi.com/flags/AX.svg",
                languages={
                    LanguagesInfoDTO(
                        name="Swedish",
                        native_name="svenska"
                    )
                },
                name="\u00c5land Islands",
                population=28875,
                subregion="Northern Europe",
                timezones=[
                    "UTC+02:00",
                ],
            ),
            weather=WeatherInfoDTO(
                temp=13.92,
                pressure=1023,
                humidity=54,
                wind_speed=4.63,
                description="scattered clouds",
                visibility=10000,
                dt=661870592,
                timezone=7200,
            ),
            currency_rates={
                "EUR": 0.016503,
            },
        )
    """

    location: CountryDTO
    weather: WeatherInfoDTO
    currency_rates: dict[str, float]
