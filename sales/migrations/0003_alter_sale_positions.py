# Generated by Django 4.1.3 on 2023-07-14 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_sale_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='positions',
            field=models.ManyToManyField(null=True, to='sales.position'),
        ),
    ]