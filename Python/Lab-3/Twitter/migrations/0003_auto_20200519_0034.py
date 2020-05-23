# Generated by Django 3.0.6 on 2020-05-18 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('Twitter', '0002_auto_20200519_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='contenttypes.ContentType'),
        ),
    ]
