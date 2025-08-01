from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from materials.models import Course, Lesson
from users.models import User


class LessonsTestCase(APITestCase):
    def setUp(self):
        # Создаем модератора
        self.moder_group = Group.objects.create(name="moders")
        self.moder = User.objects.create(email="moder@mail.ru")
        self.moder.groups.add(self.moder_group)

        # Создаем базового пользователя
        self.user = User.objects.create(email="test@mail.ru")

        # Создаем болванку-курс, для возможности создавать уроки
        self.course = Course.objects.create(name="Test", description="Test")

        # Создаем урок с незаданным владельцем
        self.lesson = Lesson.objects.create(name="Test_None", description="Test", course=self.course)

        # И с заданным
        self.his_lesson = Lesson.objects.create(
            name="Test_None", description="Test", course=self.course, owner=self.user
        )

    def test_user_can_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_create")
        data = {
            "name": "Test",
            "description": "Test",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response_data["name"], data["name"])

        self.assertEqual(response_data["owner"], self.user.id)

    def test_moder_cant_create_lesson(self):
        self.client.force_authenticate(user=self.moder)

        url = reverse("materials:lesson_create")
        data = {
            "name": "Test",
            "description": "Test",
            "course": self.course.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_retrieve_his_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson", args=[self.his_lesson.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_retrieve_not_his_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson", args=[self.lesson.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moder_can_retrieve_lesson(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lesson", args=[self.lesson.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_his_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_update", args=[self.his_lesson.pk])

        update_data = {"name": "Updated Test"}

        response = self.client.patch(url, update_data)

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response_data["name"], update_data["name"])

    def test_user_cant_update_not_his_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_update", args=[self.lesson.pk])

        update_data = {"name": "Updated Test"}

        response = self.client.patch(url, update_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moder_can_update_lesson(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lesson_update", args=[self.his_lesson.pk])

        update_data = {"name": "Updated Test From Moder"}

        response = self.client.patch(url, update_data)

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response_data["name"], update_data["name"])

    def test_user_can_delete_his_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_delete", args=[self.his_lesson.pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_not_his_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_delete", args=[self.lesson.pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moder_cant_delete_lesson(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lesson_delete", args=[self.lesson.pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_sub_and_unsub(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscription")

        data = {"id": self.course.id}

        response = self.client.post(url, data)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["message"], "Подписка добавлена")

        response_2 = self.client.post(url, data)
        response_data_2 = response_2.json()

        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data_2["message"], "Подписка удалена")
