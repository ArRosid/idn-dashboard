from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics
from course.models import (
    Training,
    TrainingCategory,
    Scheddule,
    MonthYearScheddule,
    Registration,
)
from marketing.models import Interaksi
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


def peserta_online(request):
    training = []
    data = []

    registration = Registration.objects.filter(Q(training_type=1))
    online_registration = registration.filter(Q(status=2) | Q(status=3))

    all_training = Training.objects.all()

    for t in all_training:
        training.append(t.name)
        count = len(online_registration.filter(training=t))
        data.append(count)

    # shorting based on jumlah peserta (data)
    zipped_lists = zip(data, training)
    sorted_pairs = sorted(zipped_lists, reverse=True)
    tuples = zip(*sorted_pairs)
    data, training = [list(tuple) for tuple in tuples]

    return JsonResponse(data={"labels": training, "data": data})


def peserta_offline(request):
    training = []
    data = []

    registration = Registration.objects.filter(Q(training_type=0))
    offline_registration = registration.filter(Q(status=2) | Q(status=3))

    all_training = Training.objects.all()

    for t in all_training:
        training.append(t.name)
        count = len(offline_registration.filter(training=t))
        data.append(count)

    # shorting based on jumlah peserta (data)
    zipped_lists = zip(data, training)
    sorted_pairs = sorted(zipped_lists, reverse=True)
    tuples = zip(*sorted_pairs)
    data, training = [list(tuple) for tuple in tuples]

    return JsonResponse(data={"labels": training, "data": data})


# jumlah yg daftar, baik yg bayar / tidak
# based on created_at
def pendaftar_bulanan(request):
    queryset = Registration.objects.all().order_by("created_at")
    data = {}
    for q in queryset:
        created_at = q.get_created_at_month_year()
        if created_at not in data:
            data[created_at] = 1
        else:
            data[created_at] += 1

    bulan = list(data.keys())
    jumlah = list(data.values())

    return JsonResponse(data={"labels": bulan, "data": jumlah})


# jumlah yg daftar & bayar
# based on created_at
def peserta_bayar_bulanan(request):
    queryset = Registration.objects.all().order_by("created_at")
    queryset = queryset.filter(Q(status=2) | Q(status=3))
    data = {}
    for q in queryset:
        created_at = q.get_created_at_month_year()
        if created_at not in data:
            data[created_at] = 1
        else:
            data[created_at] += 1

    bulan = list(data.keys())
    jumlah = list(data.values())

    return JsonResponse(data={"labels": bulan, "data": jumlah})


# jumlah peserta pada bulan itu
# based on jadwal
def peserta_bulanan(request):
    pass


def interaksi_last_month(request):
    last_month_interaksi = []
    month = timezone.now().month
    queryset = Interaksi.objects.all()

    dict_data = {}

    for q in queryset:
        if q.created_at.month == month:
            last_month_interaksi.append(q)

    for interaksi in last_month_interaksi:

        # kalau belum punya data tentang tgl tersebut
        if interaksi.created_at.day not in dict_data:
            dict_data[interaksi.created_at.day] = 1

        # kalau sudah punya data tentang tgl tersebut
        else:
            dict_data[interaksi.created_at.day] += 1

    hari = list(dict_data.keys())
    jumlah = list(dict_data.values())

    return JsonResponse(data={"labels": hari, "data": jumlah})
