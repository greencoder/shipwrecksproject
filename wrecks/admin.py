from django.contrib import admin

from wrecks.models import Wreck

class WreckAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

admin.site.register(Wreck, WreckAdmin)