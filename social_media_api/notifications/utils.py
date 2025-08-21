from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(*, recipient, actor, verb: str, target=None):
    if recipient == actor:
        return None  # don't notify self actions
    target_ct = None
    target_id = None
    if target is not None:
        target_ct = ContentType.objects.get_for_model(target.__class__)
        target_id = target.pk
    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=target_ct,
        target_object_id=target_id,
    )
