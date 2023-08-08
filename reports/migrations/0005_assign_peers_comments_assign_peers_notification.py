# Generated by Django 4.1.3 on 2023-07-28 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_assign_peers_assigned_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign_peers',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assign_peers',
            name='notification',
            field=models.CharField(blank=True, choices=[('NOTIFIED', 'NOTIFIED'), ('VIEWED', 'VIEWED')], max_length=100, null=True),
        ),
    ]
