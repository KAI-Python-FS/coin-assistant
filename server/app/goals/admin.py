from django.contrib import admin

from server.app.goals import models

admin.site.register(models.Goal)
