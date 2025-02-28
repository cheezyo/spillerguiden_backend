from django.db import models
from tinymce.models import HTMLField


class TechnicalPart(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class SituationType(models.Model):
    CATEGORY_CHOICES = [
        ("Mentalt", "Mentalt"),
        ("Taktisk", "Taktisk"),
        ("Fysisk", "Fysisk"),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES)  # ✅ Restricts types to a category

    def __str__(self):
        return f"{self.name} ({self.category})"  # ✅ Now displays properly


# Technical Level Model
class TechnicalLevel(models.Model):
    name = models.CharField(max_length=100)
    description = HTMLField()
    video_url = models.URLField(blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True)
    order_number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


class TournamentType(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(default="", max_length=10)

    def __str__(self):
        return str(self.name)


# Level Model
class Level(models.Model):
    name = models.CharField(max_length=100)
    short_desc = models.CharField(default=" ", max_length=200)
    description = HTMLField()
    order_number = models.IntegerField(default=0)
    required_technical_level = models.ForeignKey("TechnicalLevel",
                                                 on_delete=models.SET_NULL,
                                                 null=True,
                                                 blank=True)
    video_url = models.URLField(blank=True, null=True)
    coaching_hours = models.IntegerField(default=0)
    own_practice_hours = models.IntegerField(default=0)
    physical_hours = models.IntegerField(default=0)
    other_sports_hours = models.IntegerField(default=0)
    weeks_of_holiday = models.IntegerField(default=0)
    number_of_tournaments = models.IntegerField(default=0)
    singles_matches = models.IntegerField(default=0)
    doubles_matches = models.IntegerField(default=0)
    type_of_tournament = models.ManyToManyField(TournamentType)
    need_to_travel_abroad = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


# Player Model
class Player(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    current_level = models.ForeignKey("Level",
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    current_technical_level = models.ForeignKey("TechnicalLevel",
                                                on_delete=models.SET_NULL,
                                                null=True,
                                                blank=True)

    def __str__(self):
        return str(self.name)


# Task Model
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True)
    picture_desc = HTMLField(blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    situation_type = models.ForeignKey(SituationType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


# Progress Tracking Model
class PlayerProgress(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.name} - {self.task.name} - {'Completed' if self.is_completed else 'In Progress'}"


class TechnicalLevelTasks(models.Model):
    CATEGORY_CHOICES = [
        ('Forehand', 'Forehand'),
        ('Backhand', 'Backhand'),
        ('Serve', 'Serve'),
        ('Retur', 'Retur'),
        ('Volley', 'Volley'),
        ('Smash', 'Smash'),
        ('Forarbeid', 'Forarbeid'),
    ]
    category = models.CharField(max_length=10,
                                choices=CATEGORY_CHOICES,
                                default='Serve')
    name = models.CharField(max_length=200)
    technical_part = models.ForeignKey("TechnicalPart",
                                       on_delete=models.CASCADE,
                                       null=True,
                                       blank=True)
    description = models.TextField()
    technical_level = models.ForeignKey("TechnicalLevel",
                                        on_delete=models.CASCADE)
    video_url = models.URLField(blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True)
    picture_desc = HTMLField(default="")

    def full_name(self):
        return f"{self.category} - {self.name}"

    def __str__(self):
        return str(self.name)


class Diagnosis(models.Model):

    technical_level_task = models.ForeignKey(
        "TechnicalLevelTasks",
        on_delete=models.CASCADE,
        related_name="diagnoses"  # ✅ Set a valid default TechnicalLevelTask ID
    )
    name = models.CharField(max_length=200)  # Diagnosis name
    diagnosis = HTMLField()  # Explanation of the issue
    diagnosis_video_url = models.URLField(blank=True,
                                          null=True)  # Video for diagnosis
    diagnosis_picture_url = models.URLField(blank=True,
                                            null=True)  # Picture for diagnosis
    measure = HTMLField()  # Fix / recommendation
    measure_picture_url = models.URLField(blank=True,
                                          null=True)  # Picture for fix

    def __str__(self):
        return f"{self.name} ({self.diagnosis} - {self.technical_level_task.name})"


class CoachReport(models.Model):
    coach_name = models.CharField(max_length=255)  # ✅ Coach's Name
    player_name = models.CharField(
        max_length=255)  # ✅ Player's Name (Manual Entry)
    technical_level = models.ForeignKey(
        "TechnicalLevel",
        on_delete=models.CASCADE)  # ✅ Selected Technical Level
    tasks = models.ManyToManyField("TechnicalLevelTasks")  # ✅ Selected Tasks
    diagnoses = models.ManyToManyField("Diagnosis")  # ✅ Selected Diagnoses
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Report Date

    def __str__(self):
        return f"Report for {self.player_name} ({self.technical_level.name})"


class Drill(models.Model):
    name = models.CharField(max_length=200)
    description = HTMLField()
    video_url = models.URLField(blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True)
    situation_type = models.ForeignKey(
        "SituationType",
        on_delete=models.CASCADE,
        related_name="drills",
        null=False,  # ✅ Temporarily allow NULL
        blank=False,  # ✅ Allow blank values
    )
    suggested_time = models.PositiveIntegerField(default=10)
    category = models.CharField(max_length=20,
                                choices=[("Feeding", "Feeding"),
                                         ("Semi-Live", "Semi-Live"),
                                         ("Live", "Live")],
                                default="Feeding")

    def __str__(self):
        return str(self.name)


max_length = 20,


# ✅ New Training Plan Model
class TrainingPlan(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return str(self.name)


# ✅ Training Plan & Drill Relationship
class TrainingPlanDrill(models.Model):
    training_plan = models.ForeignKey("TrainingPlan",
                                      on_delete=models.CASCADE,
                                      related_name="plan_drills")
    drill = models.ForeignKey("Drill",
                              on_delete=models.CASCADE,
                              related_name="drill_plans")
    selected_level = models.ForeignKey(
        "Level",
        on_delete=models.CASCADE,
        null=False,  # ✅ Temporarily allow NULL
        blank=False,
    )  # ✅ NEW: Store selected level
    time_allocated = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.time_allocated:
            self.time_allocated = self.drill.suggested_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.drill.name} in {self.training_plan.name} ({self.selected_level.name}, {self.time_allocated} min)"


# ✅ New Mental Task Model
class MentalTask(models.Model):
    name = models.CharField(max_length=200)
    description = HTMLField()
    level = models.ForeignKey("Level",
                              on_delete=models.CASCADE,
                              related_name="mental_tasks")
    drills = models.ManyToManyField("Drill", blank=True)
    category = models.CharField(
        max_length=50,  # Added max_length
        choices=[
            ("In-match", "In-match"),
            ("Pre-match", "Pre-match"),
            ("Gameplan", "Gameplan"),
        ])

    def __str__(self):
        return str(self.name)


# ✅ New Physical Task Model
class PhysicalTask(models.Model):
    name = models.CharField(max_length=200)
    description = HTMLField()
    level = models.ForeignKey("Level",
                              on_delete=models.CASCADE,
                              related_name="physical_tasks")
    drills = models.ManyToManyField("Drill", blank=True)
    category = models.CharField(
        max_length=50,  # Added max_length
        choices=[
            ("Endurance", "Endurance"),
            ("Strength", "Strength"),
            ("Mobility", "Mobility"),
        ])

    def __str__(self):
        return str(self.name)


class KeyPoint(models.Model):
    drill = models.ForeignKey("Drill",
                              on_delete=models.CASCADE,
                              related_name="key_points")
    level = models.ForeignKey("Level",
                              on_delete=models.CASCADE,
                              related_name="key_points")
    description = models.TextField(
        null=True,  # ✅ Temporarily allow NULL
        blank=True,
    )

    def __str__(self):
        return f"{self.drill.name} - {self.level.name} Key Point"
