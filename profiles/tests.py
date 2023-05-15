from django.test import TestCase
from django.urls import reverse
from .models import Profile
from django.contrib.auth.models import User


class TestProfileIndex(TestCase):
    def test_profile_index(self):

        url = reverse("profiles:index")
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"<title>Profiles</title>" in response.content
        self.assertTemplateUsed(response, "profiles/index.html")


class TestProfile(TestCase):

    def test_profile_detail(self):

        user = User.objects.create(username="Mytest", email="raphael@test.com",
                                   first_name="Raphael", last_name="Hunold",
                                   password="123")
        profile = Profile.objects.create(user=user, favorite_city="Lyon")
        username = profile.user.username

        url = reverse('profiles:profile', args=[username])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response, f"{profile.user.username}")
        # assert b"<title>Mytest</title>" in response.content
        # assert b"<p>Favorite city: Lyon</p>" in response.content
