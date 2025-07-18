from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser

from materials.mixins import GetQuerysetMixin
from materials.models import Course
from materials.serializers import CourseSerializer, LessonSerializer, CourseRetrieveSerializer
from users.permissions import IsModer


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name="moders").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseRetrieveSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModer]
        elif self.action == "destroy":
            self.permission_classes = [~IsModer | IsAdminUser]
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = [IsModer | IsAdminUser]
        return [permissions() for permissions in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPEView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(GetQuerysetMixin, generics.ListAPIView):
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(GetQuerysetMixin, generics.RetrieveAPIView):
    serializer_class = LessonSerializer


class LessonUpdateAPIView(GetQuerysetMixin, generics.UpdateAPIView):
    serializer_class = LessonSerializer


class LessonDestroyAPIView(GetQuerysetMixin, generics.DestroyAPIView):
    permission_classes = [~IsModer | IsAdminUser]
