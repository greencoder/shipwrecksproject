from django.contrib import admin

from wrecks.models import Wreck
from wrecks.models import WreckType

class WreckAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_sunk', 'depth_meters', 'location')
    list_filter = ('source', 'wreck_type')

admin.site.register(Wreck, WreckAdmin)
admin.site.register(WreckType)