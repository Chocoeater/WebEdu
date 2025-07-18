from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials import views


app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', views.LessonCreateAPEView.as_view(), name='lesson_create'),
    path('lessons/', views.LessonListAPIView.as_view(), name='lessons_list'),
    path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson'),
    path('lesson/<int:pk>/update/', views.LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete/', views.LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls