from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.mixins import GetQuerysetMixin
from materials.models import Course, Lesson, Subscription
from materials.paginators import MyPaginator
from materials.serializers import CourseSerializer, LessonSerializer, CourseRetrieveSerializer
from materials.tasks import send_about_sub, send_update_sub
from users.permissions import IsModer, IsOwner


# Create your views here.


class CourseViewSet(GetQuerysetMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MyPaginator

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

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        course = self.get_object()
        subs = Subscription.objects.filter(course=course)
        user_email_list = [sub.user.email for sub in subs]

        if user_email_list:
            send_update_sub.delay(user_email_list, course.name)

        return response



class LessonCreateAPEView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(GetQuerysetMixin, generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPaginator


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


class SubscriptionAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Добавление/удаление подписки на обновления курса",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["id"],
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID курса для подписки", example=1),
            },
        ),
        responses={
            200: openapi.Response(
                description="Успешное выполнение",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Подписка добавлена"),
                    },
                ),
                examples={"application/json": {"message": "Подписка добавлена"}},
            ),
            400: openapi.Response(
                description="Ошибка валидации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(type=openapi.TYPE_STRING, example="Course ID is required"),
                    },
                ),
            ),
            404: openapi.Response(
                description="Курс не найден",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Not found."),
                    },
                ),
            ),
        },
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("id")
        course_item = get_object_or_404(Course, id=course_id)
        subscribed = Subscription.objects.filter(user=user, course=course_item).exists()

        if not course_id:
            return Response({"error": "Course ID is required"}, status=400)

        if subscribed:
            Subscription.objects.filter(user=user, course=course_item).delete()
            message = "Подписка удалена"
            send_about_sub.delay(message, user.email)
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
            send_about_sub.delay(message, user.email)

        return Response({"message": message})
