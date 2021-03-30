from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Address(models.Model):
    ADDRESS_TYPE_CHOICE = [
        ('HOME', 'HOME'),
        ('WORK', 'WORK'),
        ('Other', 'Other'),
    ]

    address_type = models.CharField(max_length=100,
                                    choices=ADDRESS_TYPE_CHOICE,
                                    default=models.BLANK_CHOICE_DASH,
                                    verbose_name='Address Type')

    detail_addr = models.CharField(max_length=150,
                                   default='Address',
                                   verbose_name='Address'
                                   )

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.first_name

