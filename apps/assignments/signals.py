from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.notifications.models import Notification
from apps.users.models import User

@receiver(post_save, sender=Assignment)
def notify_students_on_new_assignment(sender, instance, created, **kwargs): 
    if created:
        lecture = instance.lecture
        students = User.objects.filter(role='student')  

        for student in students:
            Notification.objects.create(
                user=student,
                title=f"New Assignment: {instance.title}",
                body=f"A new assignment has been added for lecture '{lecture.title}'. Due: {instance.due_date}",
                action_type='new_assignment',
                target_type='assignment',
                target_id=instance.id
            )

        # إرسال بريد إلكتروني
        from django.core.mail import send_mail
        emails = [student.email for student in students if student.email]
        send_mail(
            subject='📝 New Assignment Available',
            message=f'''
            A new assignment has been added.

            Title: {instance.title}
            Lecture: {lecture.title}
            Due Date: {instance.due_date}

            Please check the platform to submit your work on time.
            ''',
            from_email='noreply@englishlearning.com',
            recipient_list=emails,
            fail_silently=False
        )
