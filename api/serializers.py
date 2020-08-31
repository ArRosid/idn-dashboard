from rest_framework import serializers
from course.models import Training, Scheddule, DayScheddule, Registration


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


class RegistrationSerializer(serializers.ModelSerializer):
    training = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Registration
        fields = ("id", "training")
