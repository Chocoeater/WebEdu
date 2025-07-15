from rest_framework import serializers

from materials.models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

class CourseRetrieveSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)


    def get_count_lessons(self, obj):
        return obj.lessons.all().count()

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'count_lessons', 'lessons')


