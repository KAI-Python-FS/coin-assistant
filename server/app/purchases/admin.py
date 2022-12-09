from django.contrib import admin

from server.app.purchases import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Purchase)
