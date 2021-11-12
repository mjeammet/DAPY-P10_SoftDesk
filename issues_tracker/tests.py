from django.test import TestCase

# Create your tests here.
class ProjectCategory(ShopAPITestCase):

    def test_detail(self):
        # Nous utilisons l'url de détail
        url_detail = reverse('projects-detail',kwargs={'pk': self.category.pk})
        response = self.client.get(url_detail)
        # Nous vérifions également le status code de retour ainsi que les données reçues
        self.assertEqual(response.status_code, 200)
        expected = {
            'id': self.category.pk,
            'name': self.category.name,
            'date_created': self.format_datetime(self.category.date_created),
            'date_updated': self.format_datetime(self.category.date_updated),
            'products': self.get_product_detail_data(self.category.products.filter(active=True)),
        }
        self.assertEqual(expected, response.json())