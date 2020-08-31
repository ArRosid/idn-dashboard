from django.urls import path
from api.views import (
    TrainingList,
    SchedduleList,
    peserta_online,
    peserta_offline,
    pendaftar_bulanan,
    peserta_bayar_bulanan,
    interaksi_last_month,
    RegistrationUserList
)

app_name = "api"

urlpatterns = [
    path("trainings/", TrainingList.as_view(), name="TrainingList"),
    path("scheddules/", SchedduleList.as_view(), name="SchedduleList"),
    path("peserta_online/", peserta_online, name="peserta_online"),
    path("peserta_offline/", peserta_offline, name="peserta_offline"),
    path("pendaftar_bulanan/", pendaftar_bulanan, name="pendaftar_bulanan"),
    path("peserta_bayar_bulanan/", peserta_bayar_bulanan, name="peserta_bayar_bulanan"),
    path("interaksi_bulanan/", interaksi_last_month, name="interaksi_bulanan"),
    path("registration_user_list/", RegistrationUserList.as_view(), name="RegistrationUserList"),
]
