from django_filters import rest_framework as filters
from chats.models import Message


class MessageFilter(filters.FilterSet):
    # Filter by participant UUID
    user = filters.UUIDFilter(field_name='conversation__participants__id', lookup_expr='exact')

    # Filter by conversation UUID
    conversation = filters.UUIDFilter(field_name='conversation__id', lookup_expr='exact')

    # Filter by date range (ISO datetime strings)
    start_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'conversation', 'start_date', 'end_date']