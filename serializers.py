from rest_framework import serializers
from .models import Level, Task, TechnicalLevel, TechnicalLevelTasks, SituationType, TournamentType, CoachReport, TechnicalPart, Diagnosis


class CoachReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoachReport
        fields = "__all__"


class TournamentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TournamentType
        fields = '__all__'


class TechnicalLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalLevel
        fields = '__all__'


class SituationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SituationType
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    required_technical_level = TechnicalLevelSerializer(read_only=True)

    class Meta:
        model = Level
        fields = '__all__'  # Include all fields in JSON response


class TaskSerializer(serializers.ModelSerializer):
    situation_type = SituationTypeSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class TechnicalPartSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalPart
        fields = "__all__"


class TechnicalLevelTasksSerializer(serializers.ModelSerializer):
    technical_part = TechnicalPartSerializer()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = TechnicalLevelTasks
        fields = "__all__"

    def get_full_name(self, obj):
        return obj.full_name()


class DiagnosisSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="technical_level_task.category",
                                     read_only=True)
    technical_part = serializers.CharField(
        source="technical_level_task.technical_part.name", read_only=True)

    class Meta:
        model = Diagnosis
        fields = [
            "id",
            "technical_level_task",
            "category",  # ✅ Automatically fetched from the related task
            "technical_part",  # ✅ Automatically fetched from the related task
            "name",
            "diagnosis",
            "diagnosis_video_url",
            "diagnosis_picture_url",
            "measure",
            "measure_picture_url",
        ]
