import cloudinary.uploader
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Lecture
from .serializers import LectureSerializer

class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write access only for teachers
        return hasattr(request.user, 'lecture_teacher')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.teacher.user == request.user

class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user

        # Check if user is linked to a Teacher profile
        if not hasattr(user, 'lecture_teacher'):
            raise PermissionDenied("User is not registered as a teacher.")

        video_file = self.request.FILES.get('video')
        pdf_file = self.request.FILES.get('pdf')

        video_url = serializer.validated_data.get('video')

        if pdf_file:
            try:
                uploaded_pdf = cloudinary.uploader.upload(
                    pdf_file,
                    resource_type="raw",
                    format="pdf",
                    use_filename=True,
                    unique_filename=False,
                    overwrite=True,
                    access_mode="public"
                )
                pdf_url = uploaded_pdf.get('secure_url')
            except Exception as e:
                raise ValidationError(f"PDF upload failed: {str(e)}")
        else:
            pdf_url = None

        serializer.validated_data['video'] = video_url
        serializer.validated_data['pdf'] = pdf_url

        serializer.save(
            teacher=user.lecture_teacher,
            video=video_url,
            pdf=pdf_url
        )

    def perform_update(self, serializer):
        video_file = self.request.FILES.get('video')
        pdf_file = self.request.FILES.get('pdf')

        video_url = serializer.validated_data.get('video')

        if pdf_file:
            try:
                uploaded_pdf = cloudinary.uploader.upload(
                    pdf_file,
                    resource_type="raw",
                    format="pdf",
                    use_filename=True,
                    unique_filename=False,
                    overwrite=True,
                    access_mode="public"
                )
                pdf_url = uploaded_pdf.get('secure_url')
            except Exception as e:
                raise ValidationError(f"PDF upload failed: {str(e)}")
        else:
            pdf_url = serializer.instance.pdf  # Keep old PDF if no new file is uploaded

        serializer.validated_data['video'] = video_url
        serializer.validated_data['pdf'] = pdf_url

        serializer.save(
            teacher=self.request.user.lecture_teacher,
            video=video_url,
            pdf=pdf_url
        )

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'lecture_teacher'):
            return Lecture.objects.filter(teacher=user.lecture_teacher).order_by('-created_at')
        elif hasattr(user, 'student'):
            return Lecture.objects.filter(students=user.student).order_by('-created_at')
        return Lecture.objects.none()
