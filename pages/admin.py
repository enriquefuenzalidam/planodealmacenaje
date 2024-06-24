from django.contrib import admin
from . import models

admin.site.register(models.Entry)
admin.site.register(models.Description)
admin.site.register(models.Number)
admin.site.register(models.Date)
admin.site.register(models.Image)
admin.site.register(models.File)
