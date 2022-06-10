from .forms import CustomAppUserCreationForm, CustomAppUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User


class AppUserAdmin(UserAdmin):
    add_form = CustomAppUserCreationForm
    form = CustomAppUserChangeForm

    list_display = ('id', 'uid', 'username', 'email', 'cid', 'app_name')
    list_display_links = ('uid', 'username', 'email')
    list_filter = ('cid', "app_name")

    add_fieldsets = (
        ("Identification", {"fields": ("username", "email")}),
        ("Security", {"fields": ("password1", "password2")}),
    )

    fieldsets = (
        ("Creator Details", {"fields": ("cid", "app_name")}),
        ("Identification", {"fields": ("id", "uid", "username", "email", "password"), }),
        ("Bio", {"fields": ("first_name", "last_name", "other_name", "dob", "gender", "about"), }),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser"), }),
        ("Groups & Permissions", {"fields": ("groups", "user_permissions"), }),
        ("Important Dates", {"fields": ("date_joined", "last_login"), }),
    )

    readonly_fields = ('id', 'uid', 'cid', 'password', 'date_joined', 'last_login')
    ordering = ('-date_joined',)


admin.site.register(User, AppUserAdmin)
