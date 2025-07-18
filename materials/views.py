from rest_framework import viewsets, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseRetrieveSerializer
from users.permissions import ModeratorAndAdminPermission


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseRetrieveSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [ModeratorAndAdminPermission]
        return [permissions() for permissions in self.permission_classes]


class LessonCreateAPEView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorAndAdminPermission]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorAndAdminPermission]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorAndAdminPermission]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser]
