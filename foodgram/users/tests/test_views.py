from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from foodgram.tests.base_classes import ViewsTestBase

User = get_user_model()


class UsersViewsTest(ViewsTestBase):
    def setUp(self):
        self.user = User.objects.create(username='someuser')
        self.client.force_login(self.user)

    def test_template_used(self):
        reverse_names_templates = [
            (reverse('users:favorite_list'), 'users/favorite_list.html'),
            (
                reverse('users:subscription_list'),
                'users/subscription_list.html',
            ),
            (reverse('users:purchase_list'), 'users/purchase_list.html'),
            (reverse('users:registration'), 'registration/registration.html'),
            (reverse('login'), 'registration/login.html'),
            (
                reverse('password_change'),
                'registration/password_change_form.html',
            ),
            (
                reverse('password_change_done'),
                'registration/password_change_done.html',
            ),
            (
                reverse('password_reset'),
                'registration/password_reset_form.html',
            ),
            (
                reverse('password_reset_done'),
                'registration/password_reset_done.html',
            ),
            (
                # instead of reverse('password_reset_confirm')
                '/personal/auth/reset/MQ/set-password/',
                'registration/password_reset_confirm.html',
            ),
            (
                reverse('password_reset_complete'),
                'registration/password_reset_complete.html',
            ),
        ]
        self.check_template_used(reverse_names_templates)
