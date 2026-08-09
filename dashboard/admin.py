from django.contrib import admin

from dashboard.models import Tenant, Address, Room

class TenantAdmin(admin.ModelAdmin):
    list_filter = ("firstname", "lastname", "room")
    list_display = ("firstname", "lastname", "room")
    prepopulated_fields = {"slug":("firstname","lastname")}

class RoomAdmin(admin.ModelAdmin):
    list_display = ("number","room_state")

admin.site.register(Tenant, TenantAdmin)
admin.site.register(Address)
admin.site.register(Room, RoomAdmin)
