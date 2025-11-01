from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.notifications.models import Notification
from apps.users.models import User

@receiver(post_save, sender=Assignment)
def notify_students_on_new_assignment(sender, instance, created, **kwargs): 
    if created:
        lecture = instance.lecture
        students = lecture.enrolled_students.all()  

        for student in students:
            Notification.objects.create(
                user=student,
                recipient_role='student',  
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
@receiver(post_save, sender=AssignmentSubmission)
def notify_teacher_on_submission(sender, instance, created, **kwargs):
    if created:
        assignment = instance.assignment
        lecture = assignment.lecture
        teacher = lecture.teacher.user  

        Notification.objects.create(
            user=teacher,
            recipient_role='teacher',
            title=f"New Submission: {assignment.title}",
            body=f"{instance.student.user.username} has submitted the assignment.",
            action_type='submission_received',
            target_type='assignment',
            target_id=assignment.id
        )