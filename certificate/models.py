import hashlib

from django.db import models
from django.utils.translation import gettext_lazy as _
from user_profile.models import User


class CourseModule(models.Model):
    name = models.CharField(_("Module name"), max_length=350, blank=True)
    order = models.IntegerField(_("Order of the module"), default=1)

    def __str__(self):
        return self.name


class ActivityLink(models.Model):
    link = models.URLField(_("Activity link"))
    module = models.ForeignKey(CourseModule, on_delete=models.RESTRICT, related_name="activity_link")
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="user_activity")

    class Meta:
        unique_together = ('module', 'user')

    def __str__(self):
        return _("Activity %(order)s of %(user)s") % {"order": self.module.order, "user": str(self.user)}


class Certificate(models.Model):
    CHOICES = (
        ("enrollment", _("Enrollment")),
        ("certificate", _("Certificate"))
    )
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name="user_certificate")
    date_issued = models.DateTimeField(auto_now=True)
    certificate_hash = models.CharField(max_length=64, blank=True, null=True)
    certificate_type = models.CharField(max_length=12, choices=CHOICES)

    def __str__(self):
        return "(" + self.certificate_type + ") " + self.user.username + " - " + self.date_issued.strftime("%Y-%m-%d %H:%M:%S")