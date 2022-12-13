from django.contrib import admin

from server.app.operations import models


admin.site.register(models.Category)
admin.site.register(models.Operation)
