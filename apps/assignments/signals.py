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

@receiver(post_save, sender=AssignmentSubmission)
def notify_teacher_on_submission(sender, instance, created, **kwargs):
    if created:
        assignment = instance.assignment
        lecture = assignment.lecture
        teacher = lecture.teacher.user
        student_name = instance.student.user.name

        Notification.objects.create(
            user=teacher,
            title=f"{student_name} submitted assignment '{assignment.title}'",
            body=f"The student {student_name} has submitted their assignment for the lecture '{lecture.title}'.",
            action_type='assignment_submission',
            target_type='assignment',
            target_id=assignment.id
        )
