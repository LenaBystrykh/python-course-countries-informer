from django.db.models import Q, QuerySet

from geo.clients.shemas import WeatherInfoDTO
from geo.clients.weather import WeatherClient
from geo.models import Weather
from geo.services.city import CityService


class WeatherService:
    """
    Сервис для работы с данными о погоде.
    """

    def get_weather(self, alpha2code: str, city: str) -> QuerySet[Weather]:
        """
        Получение погоды по коду страны и городу.

        :param alpha2code: ISO Alpha2 код страны
        :param city: Город
        :return:
        """

        weather_db = Weather.objects.filter(
            Q(city__name__contains=city)
            | Q(city__country__alpha2code__contains=alpha2code)
        )
        if not weather_db:
            if weather_data := WeatherClient().get_weather(f"{city},{alpha2code}"):
                self.build_model(weather_data, city)
                weather_db = Weather.objects.filter(Q(city__name__contains=city))
        return weather_db

    def build_model(self, weather: WeatherInfoDTO, city: str) -> Weather:
        """
        Формирование объекта модели погоды.

        :param WeatherInfoDTO weather: Данные о погоде.
        :param str city: Город
        :return:
        """
        city = CityService().get_cities(city)[:1][0]
        weather_obj = Weather.objects.create(
            temp=weather.temp,
            pressure=weather.pressure,
            humidity=weather.humidity,
            wind_speed=weather.wind_speed,
            description=weather.description,
            visibility=weather.visibility,
            dt=weather.dt,
            timezone=weather.timezone,
            city=city,
        )
        return weather_obj
