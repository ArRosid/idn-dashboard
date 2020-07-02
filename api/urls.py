from django.urls import path
from api.views import TrainingList, SchedduleList, peserta_online

app_name = "api"

urlpatterns = [
    path("trainings/", TrainingList.as_view(), name="TrainingList"),
    path("scheddules/", SchedduleList.as_view(), name="SchedduleList"),
    path("peserta_online/", peserta_online, name="peserta_online"),
]
