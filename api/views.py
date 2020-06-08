from rest_framework import generics
from course.models import Training, TrainingCategory, Scheddule, MonthYearScheddule
from api.serializers import TrainingSerializer, SchedduleSerizlizer


class TrainingList(generics.ListAPIView):
    serializer_class = TrainingSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id")
        category = TrainingCategory.objects.get(pk=category_id)
        return Training.objects.filter(category=category)


class SchedduleList(generics.ListAPIView):
    serializer_class = SchedduleSerizlizer

    def get_queryset(self):
        training = None
        training_type = None
        month_year = None
        print(self.request.query_params)

        if self.request.query_params.get("training_id") is not None:
            training = Training.objects.get(
                id=self.request.query_params.get("training_id")
            )
        if self.request.query_params.get("training_type_id") is not None:
            training_type = self.request.query_params.get("training_type_id")
        if self.request.query_params.get("month_year_id") != "":
            month_year = MonthYearScheddule.objects.get(
                id=self.request.query_params.get("month_year_id")
            )

        data = {
            "training": training,
            "training_type": training_type,
            "month_year": month_year,
        }

        for d in data.copy():
            if data[d] is None:
                data.pop(d)
        print(data)
        return Scheddule.objects.filter(**data)
