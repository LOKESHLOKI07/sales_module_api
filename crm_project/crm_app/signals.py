from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Lead, Notification


@receiver(post_save, sender=Lead)
def notify_assigned_user(sender, instance, created, **kwargs):
    assigned_user = instance.assigned_to
    if assigned_user:
        full_name = f"{instance.first_name or ''} {instance.last_name or ''}".strip()
        message = f"You have been assigned a new lead: {full_name}"

        Notification.objects.create(user=assigned_user, message=message)

        send_mail(
            subject='New Lead Assigned',
            message=message,
            from_email='no-reply@yourcrm.com',
            recipient_list=[assigned_user.email],
            fail_silently=False,
        )
