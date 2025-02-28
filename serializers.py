from rest_framework import serializers
from .models import Level, Task, TechnicalLevel, TechnicalLevelTasks, SituationType, TournamentType, CoachReport, TechnicalPart, Diagnosis, TrainingPlan, TrainingPlanDrill, MentalTask, PhysicalTask, Drill, KeyPoint


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
    level_name = serializers.CharField(source="level.name", read_only=True)

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


class DrillSerializer(serializers.ModelSerializer):
    situation_type_name = serializers.ReadOnlyField(
        source="situation_type.name")

    class Meta:
        model = Drill
        fields = [
            "id", "name", "description", "video_url", "picture_url",
            "situation_type", "situation_type_name", "category",
            "suggested_time"
        ]


class KeyPointSerializer(serializers.ModelSerializer):
    drill_name = serializers.ReadOnlyField(source="drill.name")
    level_name = serializers.ReadOnlyField(source="level.name")

    class Meta:
        model = KeyPoint
        fields = [
            "id", "drill", "drill_name", "level", "level_name", "description"
        ]


class TrainingPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainingPlan
        fields = ["id", "name", "date"]


class TrainingPlanDrillSerializer(serializers.ModelSerializer):
    drill_name = serializers.ReadOnlyField(source="drill.name")
    selected_level_name = serializers.ReadOnlyField(
        source="selected_level.name")

    class Meta:
        model = TrainingPlanDrill
        fields = [
            "id", "training_plan", "drill", "drill_name", "selected_level",
            "selected_level_name", "time_allocated"
        ]


class MentalTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = MentalTask
        fields = "__all__"


class PhysicalTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhysicalTask
        fields = "__all__"
