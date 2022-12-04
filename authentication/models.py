from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
# Create your models here.

class User(AbstractUser):
    # address = models.CharField(max_length=254)
    is_vendor = models.BooleanField(default=False)
    is_validated =models.BooleanField(default=False)
    # company_name = models.CharField(max_length=150, blank=True, null=True)
    username_validator = RegexValidator(
                    regex=r'^\+?1?\d{9,13}$', 
                    message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed."
                    )

    username = models.CharField(
        _('username'),
        max_length=17,
        unique=True,
        help_text=_("Required. Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed."),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that Phone number already exists."),
        },
    )


    @property
    def vendor_comapny_name(self):
        return self.vendor.name



    # USERNAME_FIELD = 'phone_no'

