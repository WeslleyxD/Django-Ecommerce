from django import forms
from django.core.exceptions import ValidationError
from coupon.models import Coupon

class CouponApplyForm(forms.Form):
    code = forms.CharField()

    error_messages = {
        "coupon_not_found": ("Cupom não existe"),
        "password_small": ("A senha deve conter pelo menos 8 caracteres."),
        "email_exists": "E-mail fornecido já existe",
    }

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)
        self.user_id = user_id

    def clean(self):
        
        self.user_id
        cleaned_data = super().clean()

        try:
            Coupon.objects.get(code=cleaned_data['code'], active=True)
        except Coupon.DoesNotExist:
            raise ValidationError(
                self.error_messages["coupon_not_found"],
                code="coupon_not_found",
            )

        return cleaned_data 