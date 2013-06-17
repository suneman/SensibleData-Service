from django.contrib import admin
from .models import *

class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "description", "entry_type", "severity_lvl", "author", "payload", "_id", "_type")
    class Meta:
        verbose_name = "Audit entry admin" #TODO: add more

admin.site.register(AuditEntry, AuditEntryAdmin)

#class LoggerAdmin(admin.ModelAdmin):
#class VerifierAdmin(admin.ModelAdmin):




class AuditTrailAdmin(admin.ModelAdmin):
    list_display = ("creator", "owner", "description")
    class Meta:
        verbose_name = "Audit trail/log admin" #TODO: add more

admin.site.register(AuditTrail, AuditTrailAdmin)


