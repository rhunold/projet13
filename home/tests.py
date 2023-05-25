from django.test import TestCase
from django.urls import reverse


def test_dummy():
    assert 1


class TestHomeUrl(TestCase):
    def test_home_index(self):
        url = reverse("home:index")
        response = self.client.get(url)

        assert response.status_code == 200
        # error because of space before title end
        assert b"<title>Holiday Homes</title>" in response.content
