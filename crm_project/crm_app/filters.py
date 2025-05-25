# crm_app/filters.py
import django_filters
from .models import Lead

class LeadFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label='First Name')
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Last Name')
    status = django_filters.ChoiceFilter(choices=Lead.STATUS_CHOICES)
    assigned_to__username = django_filters.CharFilter(label="Assigned to", lookup_expr='icontains')

    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'status', 'assigned_to__username']
