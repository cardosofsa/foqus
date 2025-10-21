from django.test import TestCase
from rest_framework.test import APITestCase

class TarefasAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.login(username='testuser', password='testpass')
    
    def test_listar_tarefas(self):
        response = self.client.get('/api/tarefas/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('tarefas', response.data)