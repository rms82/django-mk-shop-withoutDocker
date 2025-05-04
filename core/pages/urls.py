from django.urls import path, include

from pages import views

app_name = "pages"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("contact_us/", views.ContactView.as_view(), name="contact_us"),
    path("about_us/", views.AboutUsView.as_view(), name="about_us"),
]
