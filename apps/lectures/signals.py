from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Lecture
from django.core.mail import send_mail
from apps.users.models import User
from apps.notifications.models import Notification


@receiver(post_save, sender=Lecture)
def send_lecture_notification(sender, instance, created, **kwargs):
    if created:
        print("📢 Notification: New lecture added →", instance.title)

        students = User.objects.filter(role='student')
        emails = [student.email for student in students]

        # إشعار داخل النظام
        for student in students:
            Notification.objects.create(
                user=student,
                title=f"New Lecture: {instance.title}",
                body=f"A new lecture has been added: {instance.description}",
                action_type='lecture_created',
                target_type='lecture',
                target_id=instance.id
            )

        # إشعار WebSocket
        channel_layer = get_channel_layer()
        data = {
            "title": instance.title,
            "teacher": instance.teacher.user.get_full_name(),
            "message": "new Lecture"
        }
        async_to_sync(channel_layer.group_send)(
            "students_group",
            {
                "type": "lecture_notification",
                "data": data
            }
        )

        # إشعار بريد إلكتروني
        send_mail(
            subject='📚 New Lecture Available',
            message=f'''
            A new lecture has been uploaded.

            Title: {instance.title}
            Description: {instance.description}
            Video Link: {instance.video or "Not available"}
            PDF File: {instance.pdf or "Not available"}
            ''',
            from_email='noreply@yourdomain.com',
            recipient_list=emails,
            fail_silently=False
        )
