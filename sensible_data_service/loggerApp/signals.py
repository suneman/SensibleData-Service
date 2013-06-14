from django.dispatch import Signal

write_to_log = Signal(
        providing_args=["user"]
        )

