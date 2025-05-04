from django.core.management.base import BaseCommand
from django.utils import timezone
from order.models import Coupon
import random
import string

class Command(BaseCommand):
    help = 'Create 100 random coupons'

    def generate_coupon_code(self, length=10):
        """Generate a random coupon code of a given length."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def handle(self, *args, **kwargs):
        coupons = []

        for _ in range(100):
            coupon_code = self.generate_coupon_code()


            discount_percent = random.randint(5, 50)  # Example range for discounts
            max_uses = random.randint(1, 100)  # Example max uses

            coupon = Coupon(
                code=coupon_code,
                discount_percent=discount_percent,
                max_uses=max_uses,
                expired=None,  # You can set this to a future date if needed
                created_date=timezone.now(),
                updated_date=timezone.now(),
            )
            coupons.append(coupon)

        # Bulk create coupons
        Coupon.objects.bulk_create(coupons)
        self.stdout.write(self.style.SUCCESS('Successfully created 100 coupons'))
