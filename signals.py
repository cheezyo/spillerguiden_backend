from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Drill, KeyPoint, Level


@receiver(post_save, sender=Drill)
def create_keypoints_for_levels(sender, instance, created, **kwargs):
    if created:
        levels = Level.objects.all()  # ✅ Get all levels
        for level in levels:
            KeyPoint.objects.create(drill=instance,
                                    level=level,
                                    description="")
