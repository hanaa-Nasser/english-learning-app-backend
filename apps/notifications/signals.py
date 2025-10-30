from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from lectures.models import Lecture
from apps.notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Lecture)
def notify_students(sender, instance, created, **kwargs):
    students = User.objects.filter(role='student')
    title = "New Lecture Added" if created else "Lecture Updated"
    body = f"Lecture Title: {instance.title}\nTeacher: {instance.teacher.user.username}"

    for student in students:
        # Save notification to the database
        Notification.objects.create(
            user=student,
            title=title,
            body=body,
            action_type="new_lecture",
            target_type="lecture",
            target_id=instance.id
        )

        # Send email to the student
        if student.email:
            send_mail(
                subject=title,
                message=body,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[student.email],
                fail_silently=True
            )
