from django.contrib.auth import get_user_model
import django_filters

# Default user model
User = get_user_model()


class UserFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['iexact'],
            'first_name': ['iexact'],
            'last_name': ['iexact'],
            'other_name': ['iexact'],
            'gender': ['iexact', ],
            'dob': ['year', 'year__gt', 'year__lt']
        }
