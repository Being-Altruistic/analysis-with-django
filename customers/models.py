from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100, blank = True)
    profile_icon = models.ImageField(upload_to='customers', default='icon.png')

    def __str__(self):
        return str(self.name)