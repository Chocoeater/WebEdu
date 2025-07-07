from django.shortcuts import render
from rest_framework import viewsets

from materials.models import Course
from materials.serializers import CourseSerializer


# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()