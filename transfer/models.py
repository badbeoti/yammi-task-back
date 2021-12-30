from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Transfer(models.Model):
    id = models.AutoField(
        primary_key=True
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    id_sender = models.IntegerField()

    id_receiver = models.IntegerField()

    amount = models.DecimalField(
        decimal_places=0,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10'))
        ]
    )

    def __str__(self):
        return str(self.id)