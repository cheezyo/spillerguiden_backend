from django.http import JsonResponse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Level, Task, TechnicalLevelTasks, TechnicalLevel, SituationType, Diagnosis, CoachReport, TechnicalPart, TrainingPlan, TrainingPlanDrill, Drill, PhysicalTask, MentalTask, KeyPoint
from .serializers import LevelSerializer, TaskSerializer, TechnicalLevelTasksSerializer, TechnicalLevelSerializer, SituationTypeSerializer, TournamentType, TournamentTypeSerializer, CoachReportSerializer, TechnicalPartSerializer, DiagnosisSerializer, TrainingPlanSerializer, TrainingPlanDrillSerializer, DrillSerializer, PhysicalTaskSerializer, MentalTaskSerializer, KeyPointSerializer
from rest_framework.decorators import action


def get_diagnoses(request):
    """ ✅ Only return diagnoses related to the selected TechnicalLevelTask """
    task_id = request.GET.get("technical_level_task")
    if task_id:
        diagnoses = Diagnosis.objects.filter(technical_level_task_id=task_id)
    else:
        diagnoses = Diagnosis.objects.all()

    data = [{
        "id": diagnosis.id,
        "name": diagnosis.name,
        "diagnosis": diagnosis.diagnosis,
        "measure": diagnosis.measure,
    } for diagnosis in diagnoses]
    return JsonResponse(data, safe=False)


@api_view(["GET"])
def chart_data(request, level_id):

    level = get_object_or_404(Level, id=level_id)
    coaching_hours = level.coaching_hours * 46
    own_hours = level.own_practice_hours * 46
    physical_hours = level.physical_hours * 46
    other_sports = level.other_sports_hours * 46
    matches = ((level.singles_matches * 1.5) + (level.doubles_matches * 1.5))
    total = coaching_hours + own_hours + physical_hours + other_sports + matches
    coaching_hours = round(coaching_hours / total * 100, 0)
    own_hours = round(own_hours / total * 100, 0)
    physical_hours = round(physical_hours / total * 100, 0)
    other_sports = round(other_sports / total * 100, 0)
    matches = round(matches / total * 100, 0)

    data = [
        {
            "name": "Med trener",
            "value": coaching_hours
        },
        {
            "name": "Egen trening",
            "value": own_hours
        },
        {
            "name": "Fysisk trening",
            "value": physical_hours
        },
        {
            "name": "Andre idretter",
            "value": other_sports
        },
        {
            "name": "Kamp",
            "value": matches
        },
    ]
    return JsonResponse(data, safe=False)


class TournamentTypeViewSet(viewsets.ModelViewSet):
    queryset = TournamentType.objects.all()
    serializer_class = TournamentTypeSerializer


class SituationTypeViewSet(viewsets.ModelViewSet):
    queryset = SituationType.objects.all()
    serializer_class = SituationTypeSerializer


# View for Levels
class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, pk=None):
        """ ✅ Retrieve a single task by ID """
        task = get_object_or_404(Task, pk=pk)
        serializer = self.get_serializer(task)
        return Response(serializer.data)


# View for Tasks
class TechnicalLevelViewSet(viewsets.ModelViewSet):
    queryset = TechnicalLevel.objects.all()
    serializer_class = TechnicalLevelSerializer

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        tasks = TechnicalLevelTasks.objects.filter(technical_level_id=pk)
        serializer = TechnicalLevelTasksSerializer(tasks, many=True)
        return Response(serializer.data)


class TechnicalPartViewSet(viewsets.ModelViewSet):
    queryset = TechnicalPart.objects.all()
    serializer_class = TechnicalPartSerializer


class TechnicalLevelTasksViewSet(viewsets.ModelViewSet):
    serializer_class = TechnicalLevelTasksSerializer

    def get_queryset(self):
        """ ✅ Allow filtering by `technical_level` in URL """
        technical_level_id = self.request.query_params.get("technical_level")
        if technical_level_id:
            return TechnicalLevelTasks.objects.filter(
                technical_level_id=technical_level_id)
        return TechnicalLevelTasks.objects.all()


@api_view(['GET'])
def get_technical_level_tasks(request, technical_level_name):
    tasks = TechnicalLevelTasks.objects.filter(
        technical_level__name=technical_level_name)
    serializer = TechnicalLevelTasksSerializer(tasks, many=True)
    return Response(serializer.data)


class CoachReportViewSet(viewsets.ModelViewSet):
    queryset = CoachReport.objects.all()
    serializer_class = CoachReportSerializer


class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

    def get_queryset(self):
        """ ✅ Allow filtering by `technical_level_task` in URL """
        technical_level_task_id = self.request.query_params.get(
            "technical_level_task")
        if technical_level_task_id:
            return Diagnosis.objects.filter(
                technical_level_task_id=technical_level_task_id)
        return Diagnosis.objects.all()


class DrillViewSet(viewsets.ModelViewSet):
    queryset = Drill.objects.all()
    serializer_class = DrillSerializer

    @action(detail=True, methods=["get"])
    def key_points(self, request, pk=None):
        """ Fetch key points for a specific drill """
        key_points = KeyPoint.objects.filter(drill_id=pk)
        serializer = KeyPointSerializer(key_points, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def count_by_situation_type(self, request):
        """ Counts drills per SituationType, only if they have key points with content for the requested level """
        level_id = request.query_params.get("level")

        if not level_id:
            return Response({"error": "Missing level parameter"}, status=400)

        drill_counts = {}

        # ✅ Loop through all drills and count only those with valid key points
        for drill in Drill.objects.all():
            # ✅ Check if the drill has key points for this level AND the key points are not empty
            valid_key_points = drill.key_points.filter(
                level_id=level_id).exclude(description="").exclude(
                    description__isnull=True)

            if valid_key_points.exists(
            ):  # ✅ Only count drills with non-empty key points
                situation_type = drill.situation_type.name if drill.situation_type else "Unknown"
                drill_counts[situation_type] = drill_counts.get(
                    situation_type, 0) + 1

        print("Drill counts (Manual Method):",
              drill_counts)  # ✅ Debugging print
        return Response(drill_counts)


class KeyPointViewSet(viewsets.ModelViewSet):
    queryset = KeyPoint.objects.all()
    serializer_class = KeyPointSerializer

    def get_queryset(self):
        """ Allow filtering key points by drill or level """
        drill_id = self.request.query_params.get("drill")
        level_id = self.request.query_params.get("level")
        queryset = self.queryset

        if drill_id:
            queryset = queryset.filter(drill_id=drill_id)
        if level_id:
            queryset = queryset.filter(level_id=level_id)

        return queryset

    @action(detail=False,
            methods=["get"],
            url_path="filter-by-drills-and-level")
    def filter_by_drills_and_level(self, request):
        """ ✅ Get Key Points filtered by Level and Drill IDs """
        level_id = request.query_params.get("level")
        drill_ids = request.query_params.get("drills")

        if not level_id or not drill_ids:
            return Response({"error": "Missing level or drills parameter"},
                            status=400)

        # ✅ Convert drill IDs from CSV format ("1,2,3") to a list
        drill_ids = drill_ids.split(",")

        # ✅ Fetch key points for the given level and drills
        key_points = KeyPoint.objects.filter(
            level_id=level_id, drill_id__in=drill_ids).exclude(
                description__isnull=True).exclude(description="")

        serializer = KeyPointSerializer(key_points, many=True)
        return Response(serializer.data)


class TrainingPlanViewSet(viewsets.ModelViewSet):
    queryset = TrainingPlan.objects.all()
    serializer_class = TrainingPlanSerializer


class TrainingPlanDrillViewSet(viewsets.ModelViewSet):
    queryset = TrainingPlanDrill.objects.all()
    serializer_class = TrainingPlanDrillSerializer


class MentalTaskViewSet(viewsets.ModelViewSet):
    queryset = MentalTask.objects.all()
    serializer_class = MentalTaskSerializer


class PhysicalTaskViewSet(viewsets.ModelViewSet):
    queryset = PhysicalTask.objects.all()
    serializer_class = PhysicalTaskSerializer
