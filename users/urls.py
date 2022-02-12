from django.urls import path
from . import views

app_name = "users"

urlpatterns = [path("me/", views.Me.as_view()), path("<int:pk>", views.UserView.as_view())]
