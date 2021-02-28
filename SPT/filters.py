import django_filters
from django_filters import DateFilter,CharFilter
from . models import Shares,Spendings

class SharesFilter(django_filters.FilterSet):
    start_date=DateFilter(field_name='date',lookup_expr='gte')
    end_date=DateFilter(field_name='date',lookup_expr='lte')
    word=CharFilter(field_name='detail',lookup_expr='icontains')
    class Meta:
        model=Spendings
        fields=['start_date','word']
