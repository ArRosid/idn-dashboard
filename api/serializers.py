from rest_framework import serializers
from course.models import Training, Scheddule, DayScheddule


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = (
            "id",
            "name",
        )


class SchedduleSerizlizer(serializers.ModelSerializer):
    day = serializers.StringRelatedField()

    class Meta:
        model = Scheddule
        fields = ("id", "day")
