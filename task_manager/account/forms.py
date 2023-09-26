from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = (
            '<ul>'
            '<li>'
            'Ваш пароль должен содержать как минимум 3 символа.'
            '</li>'
            '</ul>'
        )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
        help_text = {
            'password1': ['Один']
        }
