from django.contrib import admin

from server.app.purchases import models


admin.site.register(models.Category)
admin.site.register(models.Purchase)
