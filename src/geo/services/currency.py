from django.db.models import QuerySet, Q

from geo.clients.shemas import CurrencyRatesDTO
from geo.clients.currency import CurrencyClient
from geo.models import Currency, CurrencyRates


class CurrencyService:
    """
    Сервис для работы с данными о курсах валют.
    """

    def get_currency(self, base: str) -> QuerySet[CurrencyRates]:
        """
        Получение курса валют по названию.

        :param base: Название валюты
        :return:
        """

        currency_rates = CurrencyRates.objects.filter(Q(currency__base__contains=base))
        if not currency_rates:
            if currency_data := CurrencyClient().get_currency(base):
                currency = Currency.objects.create(
                    base=currency_data.base,
                    date=currency_data.date,
                )
                CurrencyRates.objects.bulk_create(
                    [
                        self.build_model_rates(currency, name, rate)
                        for name, rate in currency_data.rates.items()
                    ],
                    batch_size=1000,
                )
                currency_rates = CurrencyRates.objects.filter(
                    Q(currency__base__contains=currency.base)
                )
        return

    def build_model(self, currency: CurrencyRatesDTO) -> Currency:
        """
        Формирование объекта модели валюты.

        :param CurrencyRatesDTO currency: Данные о валюте.
        :return:
        """

        return Currency(
            base=currency.base,
            date=currency.date,
        )

    def build_model_rates(
        self, currency: Currency, name: str, rate: float
    ) -> CurrencyRates:
        """
        Формирование объекта модели курса валют.
        :param Currency currency: Валюта
        :param str name: Название валюты
        :param float rate: Курс валют
        :return:
        """
        return CurrencyRates(
            base_currency=currency,
            currency_name=name,
            rate=rate,
        )
