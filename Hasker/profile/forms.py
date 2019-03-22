from django import forms
from Hasker.profile.models import HaskerUser


class HaskerUserForm(forms.ModelForm):
    password_again = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = HaskerUser
        fields = ['username', 'password', 'password_again', 'email', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].required = False

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Login', 'class': 'form-control'
        })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email', 'class': 'form-control'
        })

        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password', 'type': 'password', 'class': 'form-control'
        })

        self.fields['password_again'].widget.attrs.update({
            'placeholder': 'Repeat password', 'type': 'password', 'class': 'form-control'
        })

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_again']:
            raise forms.ValidationError("Passwords mismatch")


class HaskerUserSettingsForm(HaskerUserForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False

        self.fields['username'].widget.attrs.update({'placeholder': 'Login', 'class': 'd-none'})
