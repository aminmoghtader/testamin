from django.contrib import admin

# Register your models here.
from .models import User,Car

admin.site.register(User)
admin.site.register(Car)