from django.urls import path

from accounts import views
app_name = "accounts"

urlpatterns = [
    path("list/", views.list_view, name="list"),
    path("edit/<int:user_id>/", views.edit_view, name="edit"),
    path("delete/<int:user_id>/", views.delete_view, name="delete"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.login_view, name="login"),
]
