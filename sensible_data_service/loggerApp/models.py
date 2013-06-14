from loggerApp.signals import write_to_log
from django.dispatch import receiver

@receiver(write_to_log)
def function_write_to_log(sender, **kwargs):
    return str(kwargs["user"]) # return the _id of the audit_log
