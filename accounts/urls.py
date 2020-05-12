from django.urls import path
from accounts.views import signup, activate_account


app_name = "accounts"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signup/<str:uid>/<str:token>/", activate_account, name="activate_account"),
]
