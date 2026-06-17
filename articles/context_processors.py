from .models import ContactMessage
from django.db.models import Q

def unread_messages_count(request):
    if request.user.is_authenticated:
        # Si el usuario es superusuario, ve los mensajes directos para él
        # y los mensajes generales (sin destinatario / destinatario=None)
        if request.user.is_superuser:
            count = ContactMessage.objects.filter(
                Q(destinatario=request.user) | Q(destinatario__isnull=True),
                is_read=False
            ).count()
        else:
            # Un usuario normal solo recibe mensajes dirigidos expresamente a él
            count = ContactMessage.objects.filter(
                destinatario=request.user,
                is_read=False
            ).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}
