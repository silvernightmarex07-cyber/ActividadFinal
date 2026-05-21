from django.db import migrations
from django.contrib.auth.models import User


def create_admin_user(apps, schema_editor):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, migrations.RunPython.noop),
    ]
