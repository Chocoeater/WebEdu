from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from materials.mixins import GetQuerysetMixin
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseRetrieveSerializer
from users.permissions import IsModer, IsOwner


# Create your views here.


class CourseViewSet(GetQuerysetMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseRetrieveSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsModer | IsOwner]
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        return [permissions() for permissions in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPEView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(GetQuerysetMixin, generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer | IsOwner]
