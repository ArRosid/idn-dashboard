from django.urls import path
from api.views import TrainingList, SchedduleList

app_name = "api"

urlpatterns = [
    path("trainings/", TrainingList.as_view(), name="TrainingList"),
    path("scheddules/", SchedduleList.as_view(), name="SchedduleList"),
]
