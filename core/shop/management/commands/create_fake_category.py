from django.core.management.base import BaseCommand
from faker import Faker


from shop.models import ProductCategory


class Command(BaseCommand):
    help = "Create fake products using Faker"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num", type=int, default=5, help="Number of category to create"
        )

    def handle(self, *args, **options):
        fake = Faker()
        num_category = options["num"]

        for _ in range(num_category):
            ProductCategory.objects.create(
                title=fake.word(),
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {num_category} category")
        )
