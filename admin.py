from django.contrib import admin
from django import forms
from .models import SituationType, TechnicalLevel, Level, Player, Task, PlayerProgress, TechnicalLevelTasks, SituationType, TournamentType, Diagnosis, CoachReport, TechnicalPart
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class LevelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': TinyMCE()
        },
    }


class SituationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category")  # ✅ Display both Name & Category
    list_filter = ("category", )  # ✅ Add a filter for categories
    search_fields = ("name", )  # ✅ Enable search by name


class TaskResource(resources.ModelResource):
    level = fields.Field(
        column_name='level',
        attribute='level',
        widget=ForeignKeyWidget(Level, 'name')  # ✅ Match by name, not ID
    )
    situation_type = fields.Field(
        column_name='situation_type',
        attribute='situation_type',
        widget=ForeignKeyWidget(SituationType,
                                'name')  # ✅ Match by name, not ID
    )

    class Meta:
        model = Task
        import_id_fields = ('name', )


class TaskAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TaskResource
    list_display = ("name", "category", "situation_type", "level")
    list_filter = ("category", "level")
    search_fields = ("name", "level__name")

    # ✅ Define the form field order
    fields = ("level", "category", "situation_type", "name", "description",
              "video_url", "picture_url", "picture_desc")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ ✅ Only show SituationTypes that match the Task category """
        if db_field.name == "situation_type":
            category = request.GET.get("category")  # Get selected category
            if category:
                kwargs["queryset"] = SituationType.objects.filter(
                    category=category)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TechnicalLevelTasksResource(resources.ModelResource):
    technical_level = fields.Field(
        column_name='technical_level',
        attribute='technical_level',
        widget=ForeignKeyWidget(TechnicalLevel,
                                'name')  # ✅ Match by name, not ID
    )

    class Meta:
        model = TechnicalLevelTasks
        import_id_fields = ('name', )


class TechnicalLevelTasksAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TechnicalLevelTasksResource  # ✅ Enable Import/Export
    list_display = ("name", "category", "technical_level", "diagnosis_count",
                    "add_diagnosis_link")
    list_filter = ("category", "technical_level")
    search_fields = ("name", "technical_level__name", "technical_part__name")

    def diagnosis_count(self, obj):
        """ ✅ Show number of diagnoses related to this task """
        count = Diagnosis.objects.filter(technical_level_task=obj).count()
        return count

    diagnosis_count.short_description = "Diagnoses"

    def add_diagnosis_link(self, obj):
        """ ✅ Add a 'Create Diagnosis' button for each Task """
        url = reverse(
            "admin:core_diagnosis_add") + f"?technical_level_task={obj.id}"
        return format_html('<a class="button" href="{}">➕ Add Diagnosis</a>',
                           url)

    add_diagnosis_link.short_description = "Add Diagnosis"

    def related_diagnoses(self, obj):
        """ ✅ Show a table of related diagnoses in the Task edit view """
        diagnoses = Diagnosis.objects.filter(technical_level_task=obj)
        if diagnoses.exists():
            table_html = "<table><tr><th>Name</th><th>Actions</th></tr>"
            for diagnosis in diagnoses:
                delete_url = reverse("admin:core_diagnosis_delete",
                                     args=[diagnosis.id])
                table_html += f"<tr><td>{diagnosis.name}</td><td><a href='{delete_url}'>❌ Remove</a></td></tr>"
            table_html += "</table>"
            return mark_safe(table_html)
        return "No diagnoses linked."

    related_diagnoses.short_description = "Related Diagnoses"

    fieldsets = (
        (None, {
            "fields": ("technical_level", "category", "name", "description",
                       "video_url", "picture_url", "picture_desc")
        }),
        (
            "Related Diagnoses",
            {
                "fields": ("related_diagnoses", ),
                "classes":
                ("collapse", ),  # ✅ Makes it collapsible in the admin
            }),
    )

    readonly_fields = ("related_diagnoses",
                       )  # ✅ Ensures the table is not editable


class CoachReportAdmin(admin.ModelAdmin):
    list_display = ("player_name", "coach_name", "technical_level",
                    "created_at")
    search_fields = ("player_name", "coach_name")
    filter_horizontal = ("tasks", "diagnoses"
                         )  # ✅ Allows multi-select in admin


class TechnicalPartAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )


class DiagnosisForm(forms.ModelForm):

    class Meta:
        model = Diagnosis
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Get the preselected Technical Level Task from the URL
        request = kwargs.get("request")
        if request:
            technical_level_task_id = request.GET.get("technical_level_task")
            if technical_level_task_id:
                self.fields[
                    "technical_level_task"].queryset = TechnicalLevelTasks.objects.filter(
                        id=technical_level_task_id)
                self.fields[
                    "technical_level_task"].initial = technical_level_task_id


class DiagnosisAdmin(admin.ModelAdmin):
    form = DiagnosisForm
    list_display = ("name", "technical_level_task")
    search_fields = ("name", "technical_level_task__name")


admin.site.register(TechnicalLevel)
admin.site.register(Level, LevelAdmin)
admin.site.register(Player)
admin.site.register(Task, TaskAdmin)
admin.site.register(SituationType, SituationTypeAdmin)
admin.site.register(PlayerProgress)
admin.site.register(TechnicalLevelTasks, TechnicalLevelTasksAdmin)
admin.site.register(TournamentType)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(TechnicalPart, TechnicalPartAdmin)
admin.site.register(CoachReport, CoachReportAdmin)
