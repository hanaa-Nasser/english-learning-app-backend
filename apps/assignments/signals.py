from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.notifications.models import Notification
from apps.users.models import User
from apps.users.models import Student

@receiver(post_save, sender=Assignment)
def notify_students_on_new_assignment(sender, instance, created, **kwargs): 
    if created:
        lecture = instance.lecture
        students = Student.objects.filter(is_available=True)
        for student in students:
            Notification.objects.create(
                user=student.user,
                recipient_role='student',  
                title=f"New Assignment: {instance.title}",
                body=f"A new assignment has been added for lecture '{lecture.title}'. Due: {instance.due_date}",
                action_type='new_assignment',
                target_type='assignment',
                target_id=instance.id
            )
@receiver(post_save, sender=AssignmentSubmission)
def notify_student_on_evaluation(sender, instance, created, **kwargs):
    # فقط عند التعديل وليس الإنشاء
    if not created and instance.grade is not None:
        student_user = instance.student.user
        assignment = instance.assignment

        Notification.objects.create(
            user=student_user,
            recipient_role='student',
            title=f"📊 Assignment Graded: {assignment.title}",
            body=f"You received a grade of {instance.grade}.\nFeedback: {instance.teacher_feedback or 'No comments'}",
            action_type='assignment_graded',
            target_type='assignment',
            target_id=assignment.id
        )
        # # إرسال بريد إلكتروني
        # #from django.core.mail import send_mail
        # #emails = [student.user.email for student in students if student.user.email]
        # #send_mail(
        #     subject='📝 New Assignment Available',
        #     message=f'''
        #     A new assignment has been added.

        #     Title: {instance.title}
        #     Lecture: {lecture.title}
        #     Due Date: {instance.due_date}

        #     Please check the platform to submit your work on time.
        #     ''',
        #     from_email='noreply@englishlearning.com',
        #     recipient_list=emails,
        #     fail_silently=False
        # )
@receiver(post_save, sender=AssignmentSubmission)
def notify_teacher_on_submission(sender, instance, created, **kwargs):
    print("📬 Signal triggered: AssignmentSubmission created")
    if created:
        assignment = instance.assignment
        lecture = assignment.lecture
        teacher = lecture.teacher.user  

        Notification.objects.create(
            user=teacher,
            recipient_role='teacher',
            title=f"New Submission: {assignment.title}",
            body=f"{instance.student.user.get_full_name() or instance.student.user.email} has submitted the assignment.",            action_type='submission_received',
            target_type='assignment',
            target_id=assignment.id
        )