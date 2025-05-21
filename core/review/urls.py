from django.urls import path
from .views import ReviewCreateView, ReviewDeleteView


app_name = "review"

urlpatterns = [
    path("add/", ReviewCreateView.as_view(), name="add_review"),
    path("delete/<int:pk>/", ReviewDeleteView.as_view(), name="delete_review"),
]
