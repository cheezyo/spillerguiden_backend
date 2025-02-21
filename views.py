from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Level, Task, TechnicalLevelTasks, TechnicalLevel, SituationType, Diagnosis, CoachReport, TechnicalPart
from .serializers import LevelSerializer, TaskSerializer, TechnicalLevelTasksSerializer, TechnicalLevelSerializer, SituationTypeSerializer, TournamentType, TournamentTypeSerializer, CoachReportSerializer, TechnicalPartSerializer, DiagnosisSerializer
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


# View for Tasks
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("name")
    serializer_class = TaskSerializer


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
