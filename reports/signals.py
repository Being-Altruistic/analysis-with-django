from .models import assign_peers
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# Signal to update total_sale_amount

@receiver(pre_save, sender = assign_peers)
def tag_edited(sender, instance, **kwargs):

    previous = assign_peers.objects.get(id=instance.id)
    if previous.comments != instance.comments and previous.comments != None:
        instance.comments = instance.comments+' <b>(( Edited ))</b>'
    
    instance.notification = 'NOTIFIED'

    print('******', instance.notification)



@receiver(post_save, sender = assign_peers)
def send_notification(sender, instance, **kwargs,):
    
    template_data = {
        'insobj': instance
    }

    html_body= render_to_string('reports/notification_emailtemp.html', template_data)

    msg = EmailMultiAlternatives(
        subject="You have a Notification | Go Check it out",

        body=html_body,

        from_email=instance.assigned_to.username,

        to=[instance.assigned_by.username],
    )

    msg.mixed_subtype = 'related'
    msg.attach_alternative(html_body, "text/html")

    msg.send()

