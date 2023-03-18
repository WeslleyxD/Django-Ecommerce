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
        perfil_id = kwargs.pop('perfil_id', None)
        super().__init__(*args, **kwargs)
        self.perfil_id = perfil_id

    def clean(self):
        
        self.perfil_id
        cleaned_data = super().clean()

        try:
            coupon = Coupon.objects.get(code=cleaned_data['code'], active=True)
            if coupon.perfil.id !=self.perfil_id:
               raise ValidationError(
                self.error_messages["coupon_not_found"],
                code="coupon_not_found",
            )
        except Coupon.DoesNotExist:
            raise ValidationError(
                self.error_messages["coupon_not_found"],
                code="coupon_not_found",
            )

        return cleaned_data 


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        exclude = ['perfil']