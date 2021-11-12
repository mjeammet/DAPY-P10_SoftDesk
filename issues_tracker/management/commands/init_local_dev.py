from django.contrib.auth.backends import UserModel
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

ADMIN_ID = 'admin-test'
ADMIN_PASSWORD = 'password-test'

class Command(BaseCommand):
    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        # Category.objects.all().delete()

        for data_category in CATEGORIES:
            category = Category.objects.create(name=data_category['name'],
                                               active=data_category['active'])
            for data_product in data_category['products']:
                product = category.products.create(name=data_product['name'],
                                                   active=data_product['active'])
                for data_article in data_product['articles']:
                    product.articles.create(name=data_article['name'],
                                            active=data_article['active'],
                                            price=data_article['price'])

        UserModel.objects.create_superuser(ADMIN_ID, 'admin@oc.drf', ADMIN_PASSWORD)

        self.stdout.write(self.style.SUCCESS("All Done !"))
