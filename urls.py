from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LevelViewSet, TaskViewSet, get_technical_level_tasks, TechnicalLevelViewSet, SituationTypeViewSet, TournamentTypeViewSet, chart_data, CoachReportViewSet, TechnicalPartViewSet, DiagnosisViewSet, DrillViewSet, TrainingPlanViewSet, TrainingPlanDrillViewSet, MentalTaskViewSet, PhysicalTaskViewSet, KeyPointViewSet

# Router for ModelViewSets
router = DefaultRouter()
router.register(r'levels', LevelViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'techincalLevels', TechnicalLevelViewSet)
router.register(r'situationTypes', SituationTypeViewSet)
router.register(r'tournamentTypes', TournamentTypeViewSet)
router.register(r"diagnoses", DiagnosisViewSet, basename="diagnosis")
router.register(r'technical-parts', TechnicalPartViewSet)
router.register(r"coach-reports", CoachReportViewSet, basename="coach-report")
router.register(r"drills", DrillViewSet)
router.register(r"training_plans", TrainingPlanViewSet)
router.register(r"training_plan_drills", TrainingPlanDrillViewSet)
router.register(r"mental_tasks", MentalTaskViewSet)
router.register(r"physical_tasks", PhysicalTaskViewSet)
router.register(r"keypoints", KeyPointViewSet)

urlpatterns = [
    path('api/',
         include(router.urls)),  # Include all model-based API endpoints
    path('api/technical-level-tasks/<str:technical_level_name>/',
         get_technical_level_tasks,
         name='get-technical-level-tasks'),
    path("api/chart-data/<int:level_id>/", chart_data, name="chart-data"),
    path("api/drill-counts/",
         DrillViewSet.as_view({"get": "count_by_situation_type"})),
]
