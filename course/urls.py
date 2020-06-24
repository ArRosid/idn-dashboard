from django.urls import path
from course.views import (
    daftar_training,
    delete_registration,
    edit_pendaftaran,
    payment_confirm,
    list_jadwal,
    list_jadwal_online,
    download_contoh_jadwal,
    AddJadwal,
    UpdateJadwal,
    delete_jadwal,
    list_training,
    add_training,
    UpdateTraining,
    delete_training,
    list_pembayaran,
    list_pembayaran_dp_lunas,
    list_pembayaran_ditolak,
    konfirmasi_pembayaran_dp,
    konfirmasi_pembayaran_lunas,
    hapus_konfirmasi,
    tolak_pembayaran,
    list_pendaftar_belum_bayar,
    export_pendaftar_belum_bayar,
    list_peserta,
    list_diskon,
    add_diskon,
    UpdateDiskon,
    delete_diskon,
    upload_jadwal,
    set_max_peserta,
    fu,
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
    path("list_jadwal_online/", list_jadwal_online, name="list_jadwal_online"),
    path(
        "download_contoh_jadwal/", download_contoh_jadwal, name="download_contoh_jadwal"
    ),
    path("add_jadwal/", AddJadwal.as_view(), name="add_jadwal"),
    path("update_jadwal/<int:pk>/", UpdateJadwal.as_view(), name="update_jadwal"),
    path("delete_jadwal/<int:pk>/", delete_jadwal, name="delete_jadwal"),
    path("list_training/", list_training, name="list_training"),
    path("add_training/", add_training, name="add_training"),
    path("update_training/<int:pk>/", UpdateTraining.as_view(), name="update_training"),
    path("delete_training/<int:pk>/", delete_training, name="delete_training"),
    path("list_pembayaran/", list_pembayaran, name="list_pembayaran"),
    path(
        "list_pembayaran_dp_lunas/",
        list_pembayaran_dp_lunas,
        name="list_pembayaran_dp_lunas",
    ),
    path(
        "list_pembayaran_ditolak/",
        list_pembayaran_ditolak,
        name="list_pembayaran_ditolak",
    ),
    path(
        "konfirmasi_pembayaran_dp/<int:pk>/",
        konfirmasi_pembayaran_dp,
        name="konfirmasi_pembayaran_dp",
    ),
    path(
        "konfirmasi_pembayaran_lunas/<int:pk>/",
        konfirmasi_pembayaran_lunas,
        name="konfirmasi_pembayaran_lunas",
    ),
    path("hapus_konfirmasi/<int:pk>/", hapus_konfirmasi, name="hapus_konfirmasi"),
    path("tolak_pembayaran/<int:pk>/", tolak_pembayaran, name="tolak_pembayaran"),
    path(
        "list_pendaftar_belum_bayar/",
        list_pendaftar_belum_bayar,
        name="list_pendaftar_belum_bayar",
    ),
    path(
        "export_pendaftar_belum_bayar/",
        export_pendaftar_belum_bayar,
        name="export_pendaftar_belum_bayar",
    ),
    path("list_peserta/<int:pk>/", list_peserta, name="list_peserta"),
    path("list_diskon/", list_diskon, name="list_diskon"),
    path("add_diskon/", add_diskon, name="add_diskon"),
    path("update_diskon/<int:pk>", UpdateDiskon.as_view(), name="update_diskon"),
    path("delete_diskon/<int:pk>", delete_diskon, name="delete_diskon"),
    path("upload_jadwal/", upload_jadwal, name="upload_jadwal"),
    path("set_max_peserta/", set_max_peserta, name="set_max_peserta"),
    path("fu/<int:reg_id>/", fu, name="fu"),
]
