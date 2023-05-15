from django.test import TestCase
from django.urls import reverse
from .models import Letting, Address


class TestLettingsIndex(TestCase):
    def test_lettings_index(self):

        url = reverse("lettings:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        assert b"<title>Lettings</title>" in response.content
        self.assertTemplateUsed(response, "lettings/index.html")


class TestLetting(TestCase):

    def test_letting_detail(self):
        address = Address.objects.create(number=46, street="Test Street",
                                         city="NY", state="New York",
                                         zip_code=11554, country_iso_code="USA")

        letting = Letting.objects.create(title="My Letting test", address=address)

        url = reverse('lettings:letting', kwargs={'letting_id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lettings/letting.html')
        self.assertContains(response, f"<title>{letting.title}</title>")
