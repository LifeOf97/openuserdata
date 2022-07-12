from django.contrib.auth import get_user_model
import django_filters

# Default user model
User = get_user_model()


class UserFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = User
        fields = {
            'first_name': ['exact', 'iexact'],
            'last_name': ['exact', 'iexact'],
            'other_name': ['exact', 'iexact'],
            'gender': ['exact', 'iexact', ],
            'dob': ['exact', 'year', 'year__gt', 'year__lt']
        }
