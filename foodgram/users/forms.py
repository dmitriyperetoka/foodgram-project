from django.forms import ModelForm, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Subscription

User = get_user_model()


class RegistrationForm(UserCreationForm):
    """Prompt data for creating users."""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'password1', 'password2']


class SubscriptionForm(ModelForm):
    """Prompt data for creating subscription records."""

    class Meta:
        model = Subscription
        fields = '__all__'

    def clean(self):
        user = self.cleaned_data.get('user')
        author = self.cleaned_data.get('author')

        if user and author and user == author:
            raise ValidationError('Нельзя подписываться на себя.')

        return super().clean()
