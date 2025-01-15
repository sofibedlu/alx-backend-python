import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender_id__email', lookup_expr='icontains')
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']