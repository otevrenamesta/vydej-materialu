from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Dispensed, Location, Material


class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(
        label="Heslo", widget=forms.PasswordInput(), max_length=100
    )
    location = forms.ModelChoiceField(label="Lokalita", queryset=Location.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-1"
        self.helper.field_class = "col-lg-4"
        self.helper.add_input(Submit("submit", "Přihlásit"))


class DispenseStartForm(forms.Form):
    id_card_no = forms.IntegerField(label="Číslo dokladu")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-inline mb-4"
        self.helper.field_class = "ml-3"
        self.helper.add_input(Submit("submit", "Ověřit"))


class DispenseItemForm(forms.Form):
    quantity = forms.IntegerField(label="množství", initial=0)

    def __init__(self, material, *args, **kwargs):
        super(DispenseItemForm, self).__init__(
            prefix=f"m{material.id}", *args, **kwargs
        )
        self.material = material


class DispensedForm(forms.ModelForm):
    class Meta:
        model = Dispensed
        fields = ["material", "id_card_no", "quantity"]
