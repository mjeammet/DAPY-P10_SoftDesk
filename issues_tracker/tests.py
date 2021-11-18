
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from issues_tracker.models import Project

class IssueTrackerAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(name='Test project', type="BACK")
        # Project.objects.create(name='Test inactive project', active=False)


    def get_project_details(self, project):
        expected = {
            'id': project.pk,
            'name': project.name,
            'date_created': self.format_datetime(project.date_created),
            'date_updated': self.format_datetime(project.date_updated),
            # 'issues': self.get_product_detail_data(project.issues.all()),
        }
        return expected


class TestProject(IssueTrackerAPITestCase):

    url = reverse_lazy('projects-list')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'], self.get_category_list_data([self.category, self.category_2]))


    def test_detail(self):
        # Nous utilisons l'url de détail
        url_detail = reverse('projects-detail',kwargs={'pk': self.projects.pk})
        response = self.client.get(url_detail)
        # Nous vérifions également le status code de retour ainsi que les données reçues
        self.assertEqual(response.status_code, 200)        
        self.assertEqual(self.get_project_details(self.project), response.json())
