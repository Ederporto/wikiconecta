from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class User(AbstractUser):
    groups = models.JSONField(null=True, blank=False)
    is_student = models.BooleanField(null=True, default=False)
    is_organizer = models.BooleanField(null=True, default=False)
    requested_certificate = models.BooleanField(null=True, default=False)
    date_of_request = models.DateTimeField(null=True, blank=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
    )


class UserModification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modification')
    date_of_modification = models.DateTimeField(auto_now=True)
    old_first_name = models.CharField(_("old_first_name"), max_length=150, blank=True)
    old_last_name = models.CharField(_("old_last_name"), max_length=150, blank=True)
    old_email = models.EmailField(_("old_email"), blank=True)
    new_first_name = models.CharField(_("new_first_name"), max_length=150, blank=True)
    new_last_name = models.CharField(_("new_last_name"), max_length=150, blank=True)
    new_email = models.EmailField(_("new_email"), blank=True)

    def save(self, *args, **kwargs):
        qs = UserModification.objects.filter(
            user=self.user,
            old_first_name=self.old_first_name,
            old_last_name=self.old_last_name,
            old_email=self.old_email,
            new_first_name=self.new_first_name,
            new_last_name=self.new_last_name,
            new_email=self.new_email,
        ).exclude(pk=self.pk)

        if qs.exists():
            return

        if self.old_first_name == self.new_first_name and self.old_last_name == self.new_last_name and self.old_email == self.new_email:
            return

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.__str__() + " ({})".format(self.date_of_modification.strftime("%Y-%m-%dT%H:%M:%S"))


class Participant(models.Model):
    username = models.CharField(_("username"), max_length=150, blank=True)
    last_date = models.DateTimeField(auto_now=True)

