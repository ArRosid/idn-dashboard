from django.urls import path
from course.views import (
    daftar_training,
    delete_registration,
    edit_pendaftaran,
    payment_confirm,
    list_jadwal,
    jadwal_upload,
    AddJadwal,
    UpdateJadwal,
    delete_jadwal,
    list_training,
    add_training,
    UpdateTraining,
    delete_training,
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
    path("list_jadwal/", list_jadwal, name="list_jadwal"),
    path("upload_jadwal/", jadwal_upload, name="upload_jadwal"),
    path("add_jadwal/", AddJadwal.as_view(), name="add_jadwal"),
    path("update_jadwal/<int:pk>/", UpdateJadwal.as_view(), name="update_jadwal"),
    path("delete_jadwal/<int:pk>/", delete_jadwal, name="delete_jadwal"),
    path("list_training/", list_training, name="list_training"),
    path("add_training/", add_training, name="add_training"),
    path("update_training/<int:pk>/", UpdateTraining.as_view(), name="update_training"),
    path("delete_training/<int:pk>/", delete_training, name="delete_training"),
]
