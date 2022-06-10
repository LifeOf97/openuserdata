from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Length
from django.core import validators
from django.conf import settings
from django.db import models
from typing import List
import uuid


# Register __length
models.CharField.register_lookup(Length)


# Functiuon to create random ints
def get_random_int():
    return str(uuid.uuid4().int)[:15]


GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class UserManager(BaseUserManager):
    def create_user(
        self,
        username: str,
        email: str,
        password: str = None,
        is_active: bool = True,
        is_staff: bool = False,
        is_superuser: bool = False
            ):
        if not username:
            raise ValueError(_("Users must provide a username"))
        if not email:
            raise ValueError(_("Users must provide an email address"))

        user = self.model(username=username.lower(), email=self.normalize_email(email.lower()))
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str = None,
        is_active: bool = True,
        is_staff: bool = True,
        is_superuser: bool = True
            ):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Custom User model
    """
    # Identification
    id = models.BigAutoField(_("ID"), unique=True, primary_key=True, editable=False, help_text=_("User database ID"))
    uid = models.CharField(_("UID"), max_length=15, unique=True, default=get_random_int, help_text=_("User Unique ID"))
    cid = models.CharField(_("CID"), max_length=15, blank=True, null=True, help_text=_("The creators ID"))
    app_name = models.CharField(
        _("App Name"), max_length=20, blank=True, null=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[a-zA-Z]([\w -]*[a-zA-Z])?$',
                message=_("Must begin and end with a letter. And can only contain letters, numbers and hyphens"),
            ),
            validators.MinLengthValidator(limit_value=4)
        ],
        help_text=_("The name of this Openuser data. Spaces are replaced with underscores")
    )

    # Bio
    username = models.CharField(
        _("Username"), max_length=20, blank=False, unique=True,
        validators=[
            validators.MinLengthValidator(limit_value=4),
            validators.RegexValidator(
                regex=r"\W",
                message=_("Username can only contain letters, numbers and underscore"),
                inverse_match=True
            )
        ],
        error_messages={"unique": _("This username is not available")},
    )
    email = models.EmailField(
        _("Email Address"), unique=True, max_length=255, blank=False,
        error_messages={"unique": _("This email address belongs to another account")}
    )
    password = models.CharField(
        _("Password"), max_length=128, help_text=_("User password"),
        validators=[
            validators.MinLengthValidator(limit_value=8),
            validators.RegexValidator(
                regex=r'\s',
                message=_("Password cannot contain spaces"),
                inverse_match=True
            )
        ]
    )
    first_name = models.CharField(_("First Name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=255, blank=True, null=True)
    other_name = models.CharField(_("Other Name"), max_length=255, blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=7, choices=GENDER, blank=True, null=True)
    mugshot = models.URLField(
        _("Mugshot"), max_length=255,
        blank=True, null=True,
        help_text=_("Users mugshot url")
    )
    dob = models.DateField(_("Date of Birth"), auto_now=False, auto_now_add=False, blank=True, null=True)
    about = models.TextField(_("About"), help_text=_("About me"), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD: str = 'username'
    REQUIRED_FIELDS: List[str] = ['email']

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(username__length__gte=4), name="min_username_length"),
            models.UniqueConstraint(fields=['cid', 'app_name'], name='unique_app_name'),
        ]
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        # converts usernames to lowercase and replaces spaces with underscores
        self.username = str(self.username).replace(' ', '_').lower()
        self.email = self.email.lower()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return F"{self.cid or ''}-{self.app_name or ''}-{self.username or ''}"

    def get_full_name(self) -> str:
        return F"{self.first_name or ''} {self.last_name or ''} {self.other_name or ''}"


class Address(models.Model):
    """
    Address model for the custom user model users data.
    """
    id = models.BigAutoField(_("ID"), primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE
    )
    country = models.CharField(_("Country"), max_length=255, blank=True, null=True)
    country_code = models.CharField(_("Country Code"), max_length=5, blank=True, null=True)
    state = models.CharField(_("State"), max_length=255, blank=True, null=True)
    state_abbr = models.CharField(_("State Abbreviation"), max_length=5, blank=True, null=True)
    city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    postal = models.CharField(_("Postal/ZIP"), max_length=20, blank=True, null=True)
    street = models.CharField(_("Street"), max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['country']
        verbose_name_plural = 'Addresses'
