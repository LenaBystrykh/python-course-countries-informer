"""
Функции для взаимодействия с внешним сервисом-провайдером данных о погоде.
"""
from http import HTTPStatus
from typing import Optional

import httpx

from app.settings import REQUESTS_TIMEOUT, API_KEY_OPENWEATHER
from base.clients.base import BaseClient
from geo.clients.shemas import WeatherInfoDTO


class WeatherClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о погоде.
    """

    def get_base_url(self) -> str:
        return "https://api.openweathermap.org/data/2.5/weather"

    def _request(self, endpoint: str) -> Optional[dict]:
        with httpx.Client(timeout=REQUESTS_TIMEOUT) as client:
            # получение ответа
            response = client.get(endpoint)
            if response.status_code == HTTPStatus.OK:
                return response.json()

            return None

    def get_weather(self, location: str) -> Optional[WeatherInfoDTO]:
        """
        Получение данных о погоде.

        :param location: Город и страна
        :return:
        """

        result = self._request(
            f"{self.get_base_url()}?units=metric&q={location}&appid={API_KEY_OPENWEATHER}"
        )
        return (
            WeatherInfoDTO(
                temp=result["main"]["temp"],
                pressure=result["main"]["pressure"],
                humidity=result["main"]["humidity"],
                wind_speed=result["wind"]["speed"],
                description=result["weather"][0]["description"],
                visibility=result["visibility"],
                dt=result["dt"],
                timezone=result["timezone"],
            )
            if result
            else None
        )
