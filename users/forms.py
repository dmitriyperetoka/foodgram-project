from django.forms import ModelForm, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Subscription

User = get_user_model()


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'

    def clean(self):
        user = self.cleaned_data.get('user')
        author = self.cleaned_data.get('author')

        if user and author and user == author:
            raise ValidationError('Нельзя подписываться на себя')

        return super().clean()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'password1', 'password2']
