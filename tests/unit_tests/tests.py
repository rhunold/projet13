from django.test import TestCase
from django.urls import reverse


def test_dummy():
    assert 1


class TestOcLettingsIndexUrl(TestCase):
    def test_oc_lettings_site_index(self):
        url = reverse("index")
        response = self.client.get(url)

        assert response.status_code == 200
        # error because of space before title end
        assert b"<title>Holiday Homes</title>" in response.content
