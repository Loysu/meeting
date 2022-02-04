from django_filters import rest_framework as filters

from .models import Profile


class ProfileFilter(filters.FilterSet):
    """Фильтрация профиля по полу, имени и фамилии"""
    first_name = filters.CharFilter(field_name='user__first_name', label='Имя', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='user__last_name', label='Фамилия', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ('gender', 'first_name', 'last_name')
