from django.db import models

from django.utils.translation import gettext_lazy as _


class UserRequest(models.Model):
    ip = models.CharField(_('ip'), max_length=30, unique=True)
    request_count = models.IntegerField(_('request_count'), default=1)
    request_started = models.DateTimeField(_('request_time'), auto_now_add=True, null=True)
    
    def __str__(self):
        return self.ip