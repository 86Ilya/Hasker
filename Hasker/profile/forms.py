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
        self.fields['avatar'].label = 'Upload Avatar:'
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control-file'
        })

        if self.fields.get('username', None):
            self.fields['username'].widget.attrs.update({
                'placeholder': 'Login', 'class': 'form-control mb-3'
            })
            self.fields['username'].help_text = ''
            self.fields['username'].label = ''

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email', 'class': 'form-control mb-3'
        })
        self.fields['email'].help_text = ''
        self.fields['email'].label = ''

        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password', 'class': 'form-control mb-3'
        })
        self.fields['password'].help_text = ''
        self.fields['password'].label = ''

        self.fields['password_again'].widget.attrs.update({
            'placeholder': 'Repeat password', 'class': 'form-control mb-3'
        })
        self.fields['password_again'].help_text = ''
        self.fields['password_again'].label = ''

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_again']:
            raise forms.ValidationError("Passwords mismatch")
        elif len(cleaned_data['password']) < 8:
            raise forms.ValidationError("Password length must be at least 8 symbols")
        return cleaned_data


class HaskerUserSettingsForm(HaskerUserForm):

    class Meta(HaskerUserForm.Meta):
        fields = ['password', 'password_again', 'email', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False

    def clean(self):
        cleaned_data = super().clean()
        non_empty_data = dict()
        for key, value in cleaned_data.items():
            if value:
                print(key, value)
                non_empty_data.update({key: value})

        return non_empty_data
