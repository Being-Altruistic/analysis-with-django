from django.db import models
from profiles.models import Profile
from django.contrib.auth.models import User

from django.urls import reverse
# Create your models here.


class Report(models.Model):
    name= models.CharField(max_length=120)
    image = models.ImageField(upload_to='reports', blank=True)
    remarks = models.TextField(blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("reports:detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ('-created',)
    

'''
created
updated
assignedby USER
assignedto USER
reportno   REPORT
token      UUID

'''

class assign_peers(models.Model):
    assigned_by = models.ForeignKey(User, related_name="assigned_by", on_delete=models.CASCADE, blank=True, null=True)
    assigned_to = models.ForeignKey(User, related_name="assigned_to", on_delete=models.CASCADE, blank=True, null=True)
    token = models.CharField(default='', blank=True, null=True, max_length=500)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    notification = models.CharField(max_length=100,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("reports:secured_detail", kwargs={"pk": self.report.id,"token": self.token})



    def __str__(self):
        return str(self.token)+':  '+str(self.assigned_by)+'[ > ]'+str(self.assigned_to)



