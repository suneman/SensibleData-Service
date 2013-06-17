from django.dispatch import receiver
from django.db import models

# Signals go here so they can be loaded early
#@receiver(write_to_log) 
#def function_write_to_log(sender, **kwargs):
#    return str(kwargs["user"]) # returns the _id of the audit_log



# TODO: check for the appropriate fields: timestamp/time, id/increasingInt, name/varchar, payload/???

# Models:
LENGTH = 100 #TODO: finer distinction

# Corresponds to a table entry in mongoDB
class AuditEntry(models.Model):
    timestamp = models.PositiveIntegerField()
    description = models.CharField(max_length = LENGTH)
    entry_type = models.CharField(max_length = LENGTH)
    severity_lvl = models.CharField(max_length = LENGTH)
    author = models.CharField(max_length = LENGTH) # Which entity wrote this entry
    payload = models.CharField(max_length = LENGTH) # TODO check the best way to have dynamic stuff here [old flowID]
    _id = models.PositiveIntegerField() #
    v = models.CharField(max_length = LENGTH)
    mac = models.CharField(max_length = LENGTH)
    _type = models.CharField(max_length = LENGTH) # Tag for the entry

    def __unicode__(self):
        return u"%d, &d, %s, author = %s, payload = %s" % (self.timestamp, self._id, self.severity_lvl, self.author, self.payload)

    class Meta:
        permissions = (
                ("auditEntry_append", "can append a new entry to the trail"),
                ("auditEntry_read", "can read an entry"),
                ("auditEntry_verify", "can check the integrity of a log entry"),
        )

# Corresponds to a table in mongoDB
# Different users have different trails
# Different users have different tables
class AuditTrail(models.Model):
    auditEntry = models.ForeignKey(AuditEntry) # One-to-many relation

    creator = models.CharField(max_length = LENGTH) # The entity who created this audit trail for the user
    owner = models.CharField(max_length = LENGTH) # The entity to whom this audit trail refers to (i.e.: user, admin, system, app, ...)
    creation_time = models.PositiveIntegerField() # When this audit trail has been created
    number_of_entries = models.PositiveIntegerField() # Total number of audit entries in this trail
    _id = models.PositiveIntegerField() # The unique identifier for this audit trail
    description = models.CharField(max_length = LENGTH) # Human readable description of this trail
    _type = models.CharField(max_length = LENGTH) # Tag for the audit trail (i.e.: "user log", "system log", ...)

    def __unicode__(self):
        return u"id = %d, owner = %s, entries = %d" % (self._id, self.owner, self.number_of_entries) 

    class Meta:
        permissions = (
                ("auditTrail_read", "can read the whole audit trail"),
                ("auditTrail_initialize", "can initialize an audit trail (setup)"),
                ("auditTrail_verify", "can check the integrity of the whole audit trail (hash chain check)"),
        )



