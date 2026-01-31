from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from messaging.models import User, Message
from messaging.serializer import MessageSerializer


@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = User.objects.get(pk=request.user.id)
    user.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@cache_page(60)
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def fetch_messages(request):
    message = Message.objects.filter(
        parent_message__isnull=True,
        sender=request.user
    ).select_related(
        'receiver', 'sender'
    ).prefetch_related('replies', 'replies__sender')

    serializer = MessageSerializer(message, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def fetch_unread_messages(request):
    messages = Message.unread.unread_for_user(
        request.user).only(
        'content', 'sender')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)