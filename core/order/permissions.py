from django.contrib.auth.mixins import UserPassesTestMixin

from order.models import Order, OrderStatus

class OrderCompletePermission(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
            
        try:
            order = Order.objects.get(
                user=self.request.user,
                status=OrderStatus.pending.value,
                id = self.kwargs.get("pk"),
            )
            return order.items.count() > 0
        except Order.DoesNotExist:
            return False