import random

from django.core.management.base import BaseCommand

from currency.models import Rate, Source
from currency.choices import CurrencyTypeChoices


class Command(BaseCommand):
    help = 'Genarete 500 random rates'  # noqa

    def handle(self, *args, **options):
        source, _ = Source.objects.get_or_create(
            code_name='dummy',
            defaults={
                'name': 'Dummy source'
            }
        )

        for _ in range(500):
            Rate.objects.create(
                buy=random.randint(30, 40),
                sell=random.randint(40, 50),
                source=source,
                currency_type=random.choice(CurrencyTypeChoices.choices)[0]
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated rates'))
