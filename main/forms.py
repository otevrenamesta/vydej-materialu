from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Dispensed, Location, Material


class LoginForm(forms.Form):
    username = forms.CharField(label="login", max_length=100)
    password = forms.CharField(
        label="heslo", widget=forms.PasswordInput(), max_length=100
    )
    location = forms.ModelChoiceField(label="lokalita", queryset=Location.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-7"
        self.helper.add_input(Submit("submit", "přihlásit"))


class DispenseStartForm(forms.Form):
    id_card_no = forms.IntegerField(label="číslo dokladu")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-3"
        self.helper.add_input(Submit("submit", "ověřit"))


class DispenseNewForm(forms.Form):
    material = forms.ModelChoiceField(label="materiál", queryset=Material.objects.all())
    quantity = forms.IntegerField(label="množství")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-3"
        self.helper.add_input(Submit("submit", "vydat"))


class DispensedForm(forms.ModelForm):
    class Meta:
        model = Dispensed
        fields = ["material", "id_card_no", "quantity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-7"
        self.helper.add_input(Submit("submit", "uložit"))
