from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review

@receiver([post_save, post_delete], sender=Review)
def update_hospital_avg_rating(sender, instance, **kwargs):
    hospital = instance.hospital
    reviews = Review.objects.filter(hospital=hospital)
    total_rating = sum(review.hospital_rating for review in reviews)
    average_rating = total_rating / reviews.count() if reviews.exists() else 0

    hospital.average_rating = average_rating
    hospital.num_reviews = reviews.count()
    hospital.save()