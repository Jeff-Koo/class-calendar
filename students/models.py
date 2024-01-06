from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Student(models.Model):

    name = models.CharField(blank=False, null=False, unique=True)
    phone_regex = RegexValidator(
        regex=r'^[0-9+\- ]+$',
        message="Phone number can only contain digits (0-9), plus sign (+), hyphen (-), and space ( ), but not in consecutive sequence."
    )
    phone = models.CharField(blank=True, validators=[phone_regex])
    memo = models.TextField(blank=True)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)


    def view_link(self) -> str:
        if self.url:
            return mark_safe(
                '<a href="{0}" target="_blank">{1}</a>'.format(
                    self.url, "View on site"
                )
            )
        return '-'
    
    
    def __str__(self):
        return self.name
    
    
    @property
    def url(self) -> str:
        return reverse('get_student', kwargs={'pk': self.pk})

