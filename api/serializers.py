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
    class Meta:
        model = Registration
        fields = ("id", "user", "training")

    def to_representation(self, instance):
        instance.training = Training.objects.get(id=instance.training).name
        return super(RegistrationSerializer, self).to_representation(instance)
