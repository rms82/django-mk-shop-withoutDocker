from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Product, ProductCategory, ProductStatus

from faker import Faker
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create fake products using Faker'

    def add_arguments(self, parser):
        parser.add_argument('--num', type=int, default=10, help='Number of products to create')

    def handle(self, *args, **options):
        fake = Faker()
        num_products = options['num']

        # Create some sample product categories
        categories = list(ProductCategory.objects.all())

        # Create some sample users
        users = list(User.objects.filter(is_superuser=True))

        for _ in range(num_products):
            product = Product(
                title=fake.sentence(nb_words=3),
                description=fake.text(),
                user=random.choice(users),
                stock=fake.pyint(min_value=0, max_value=100),
                status=fake.random_element([status.value for status in ProductStatus]),
                price=fake.pyint(min_value=10000, max_value=6000000),
                discount=fake.pyint(min_value=0, max_value=60),
            )
            product.save()
            product.category.set(random.sample(categories, random.randint(1,4)))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_products} products'))