from typing import Optional

from django.db.models import Q

from geo.models import Country
from geo.services.country import CountryService
from news.clients.news import NewsClient
from news.clients.shemas import NewsItemDTO
from news.models import News


class NewsService:
    """
    Сервис для работы с данными о новостях.
    """

    def get_news(self, country_code: str) -> Optional[list[News]]:
        """
        Получение актуальных новостей по коду страны.

        :param str country_code: ISO Alpha2 код страны
        :return:
        """

        news = News.objects.filter(Q(country__alpha2code__contains=country_code))
        if not news:
            if news_data := NewsClient().get_news(country_code):
                codes = CountryService().get_countries_codes()
                if codes is None or country_code not in codes:
                    CountryService().get_countries(country_code)
                    codes = CountryService().get_countries_codes()
                    if codes is None or codes.get(country_code, None) is None:
                        return None

        return NewsClient().get_news(country_code)
        news = News.objects.bulk_create(
            [
                self.build_model(news_item, codes[country_code])
                for news_item in news_data
            ],
            batch_size=1000,
        )

        return news

    def save_news(self, country_pk: int, news: list[News]) -> None:
        """
        Сохранение новостей в базе данных.

        :param country_pk: Первичный ключ страны в базе данных
        :param news: Список объектов новостей
        :return:
        """

        if news:
            News.objects.bulk_create(
                [self.build_model(news_item, country_pk) for news_item in news],
                batch_size=1000,
            )

    def build_model(self, news_item: News, country_id: int) -> News:
        """
        Формирование объекта модели новости.

        :param News news_item: Данные о новости
        :param int country_id: Идентификатор страны в БД
        :return:
        """

        return News(
            country_id=Country.objects.get(pk=country_id),
            source=news_item.source,
            author=news_item.author if news_item.author else "",
            title=news_item.title,
            description=news_item.description if news_item.description else "",
            url=news_item.url if news_item.url else "",
            published_at=news_item.published_at,
        )
