from django.urls import path

from . import views
urlpatterns = [
    # Auth
    path("accounts/login/", views.login_or_register, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),

    path("", views.chat_view, name="home"),
]
