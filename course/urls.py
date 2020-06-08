from django.urls import path
from course.views import (
    daftar_training,
    delete_registration,
    edit_pendaftaran,
    payment_confirm,
)

app_name = "course"

urlpatterns = [
    path("register/", daftar_training, name="daftar_training"),
    path("register/update/<int:pk>/", edit_pendaftaran, name="edit_pendaftaran"),
    path("register/delete/<int:pk>/", delete_registration, name="delete_registration"),
    path(
        "payment_confirm/<int:registration_id>/",
        payment_confirm,
        name="payment_confirm",
    ),
]
