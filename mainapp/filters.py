from math import cos, sin, acos, radians

from django_filters import rest_framework as filters

from .models import Profile


class ProfileFilter(filters.FilterSet):
    """Фильтрация профиля по полу, имени, фамилии и дистанции между пользователями"""
    first_name = filters.CharFilter(field_name='user__first_name', label='Имя', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='user__last_name', label='Фамилия', lookup_expr='icontains')
    distance = filters.NumberFilter(label='Расстояние (в километрах)', method='calc_distance')

    class Meta:
        model = Profile
        fields = ('gender', 'first_name', 'last_name', 'distance')

    def calc_distance(self, queryset, name, value):
        # находит расстояние между пользователями и сравнивает его с "value"
        if self.request.user.is_authenticated:
            to_be_excluded = []
            request_profile = self.request.user.profile
            for profile in queryset.all():
                # формула находит расстояние между 2-мя координатами
                distance_between_two_profiles = 6371 * acos(sin(radians(request_profile.latitude)) * sin(radians(
                    profile.latitude)) + cos(radians(request_profile.latitude)) * cos(radians(profile.latitude)) * cos(
                    radians(request_profile.longitude - profile.longitude)))
                # если переданное значение меньше, чем расстояние между пользователями,
                # то добавляем профиль второго пользователя в исключение
                if value < distance_between_two_profiles:
                    to_be_excluded.append(profile.pk)
            return queryset.exclude(pk__in=to_be_excluded)
        return queryset.none()
