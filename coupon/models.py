from datetime import timedelta, datetime
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from perfil.models import Perfil

class Coupon(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=True, related_name='coupon')
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField(auto_now_add=True, editable=False)
    valid_to = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def valited_coupon(self):
        # Valida se o copum ainda está dentro do prazo válido
        time_now = timezone.now()
        if self.valid_to >= time_now:
            return True
        else:
            self.active = False
            self.save()
            return False
    
        