from django.test import TestCase
from django.urls import reverse
from .models import Note
class NotesAppTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DevOps Notes')
    def test_create_note(self):
        response = self.client.post(reverse('create_note'), {'title': 'First note', 'content': 'Testing CI/CD'})
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Note.objects.filter(title='First note').exists())
    def test_health_endpoint(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')
