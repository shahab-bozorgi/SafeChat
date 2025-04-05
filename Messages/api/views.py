from rest_framework import viewsets
from .serializers import MessageSerializer
from ..models import Message


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
