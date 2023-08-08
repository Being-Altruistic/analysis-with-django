from django.contrib import admin
from .models import Report, assign_peers
# Register your models here.


admin.site.register(Report)
admin.site.register(assign_peers)