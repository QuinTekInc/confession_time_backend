from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Confession)
admin.site.register(models.EmailVerification)
admin.site.register(models.SavedUser)
admin.site.register(models.Reports)
admin.site.register(models.Review)