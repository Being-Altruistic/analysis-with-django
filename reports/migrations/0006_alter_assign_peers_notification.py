# Generated by Django 4.1.3 on 2023-07-28 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_assign_peers_comments_assign_peers_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assign_peers',
            name='notification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
