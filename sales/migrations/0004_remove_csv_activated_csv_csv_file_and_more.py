# Generated by Django 4.1.3 on 2023-07-15 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_alter_sale_positions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csv',
            name='activated',
        ),
        migrations.AddField(
            model_name='csv',
            name='csv_file',
            field=models.FileField(null=True, upload_to='csvs'),
        ),
        migrations.AlterField(
            model_name='csv',
            name='file_name',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='positions',
            field=models.ManyToManyField(to='sales.position'),
        ),
    ]
