from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse


from accounts.models import UserType, Profile


# Create your views here.
class RedirectToDashbordView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == UserType.customer.value:

                return redirect('dashboard:customer:customer_dashboard')

            elif request.user.user_type == UserType.admin.value:

                return redirect('dashboard:admin:admin_dashboard')
            
        return redirect('accounts:login')

class ResetProfileImageView(
    LoginRequiredMixin,
    View,
):
    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        profile.reset_image_to_default()
        return JsonResponse({
            'success': 'success'
        })


    
