from django.contrib.auth.mixins import UserPassesTestMixin

from accounts.models import UserType


class AdminDashboardPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.user_type == UserType.admin.value

        return False


class CustomerDashboardPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.user_type == UserType.customer.value

        return False
