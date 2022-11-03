import json
from django import forms
from . models import Address, Perfil
from django.core.exceptions import ValidationError
from . utils import via_cep

# Create the form class.
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
    
    error_messages = {
        "number_cep": ("Insira o CEP apenas com números."),
        "small_cep": ("O CEP deve conter 8 números."),
        "invalid_cep": ("CEP não existe.")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"login-form-attr"})
            if self.fields[field].label == 'CEP':
                self.fields[field].widget.attrs.update({"class":"login-form-attr", "required": True, "onkeypress":"mascara_cep()"})
            
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        cep = cleaned_data.get("cep")
        # try:
        #     cep = cep.replace(cep[5], '')
        # except Exception as e:
        #     raise ValidationError(
        #         self.error_messages["small_cep"],
        #         code="invalid",
        #     )
        if not cep.isnumeric():
            raise ValidationError(
                self.error_messages["number_cep"],
                code="invalid",
            )
        self.viacep = via_cep(cep)
        if not self.viacep:
            raise ValidationError(
                self.error_messages["invalid_cep"],
                code="invalid",
            )

        return cleaned_data

    def save(self, commit=True):
        form = super().save(commit=False)
        viacep = json.loads(self.viacep)
        form.cep = viacep.get('cep').replace('-', '')
        form.state = viacep.get('uf')
        form.country = viacep.get('localidade')
        form.district = viacep.get('bairro')
        form.address = viacep.get('logradouro')
        
        #form.set_password(self.cleaned_data["password1"])
        if commit:
            form.save()
        return form
        # password2 = cleaned_data.get("password2")
        # if password1 != password2:
        #     raise ValidationError(
        #         self.error_messages["invalid_password"],
        #         code="inactive",
        #     )
        # if len(password1) < 8:
        #     raise ValidationError(
        #         self.error_messages["senha_pequena"],
        #         code="inactive",
        #     )

# TODO: FAZER VALIDAÇÃO DOS FORMS
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['cpf', 'cell', 'birth', 'genre']
        widgets = {
            'birth': forms.DateInput(format = '%Y-%m-%d', attrs={'type':'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"login-form-attr"})