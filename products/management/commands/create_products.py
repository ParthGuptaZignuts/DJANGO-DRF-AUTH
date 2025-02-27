import random

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker

from products.models import Product

fake = Faker()


class Command(BaseCommand):
    help = "Generate 1000 random products"

    def handle(self, *args, **kwargs):
        products = [
            Product(
                name=fake.word().capitalize() + " " + fake.word().capitalize(),
                description=fake.sentence(nb_words=10),
                price=round(random.uniform(5.0, 500.0), 2),
                created_at=now(),
                updated_at=now(),
            )
            for _ in range(1000)
        ]

        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS("✅ Successfully created 1000 products!"))
