from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from order.models import Order, OrderStatus

class Command(BaseCommand):
    help = 'Deletes orders with pending status older than 10 minutes.'

    def handle(self, *args, **options):
        threshold_time = timezone.now() - timedelta(minutes=30)
        old_orders = Order.objects.filter(
            status=OrderStatus.pending,
            created_date__lt=threshold_time
        )
        count = old_orders.count()
        old_orders.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} unpaid orders older than 30 minutes."))