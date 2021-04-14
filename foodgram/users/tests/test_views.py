from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from foodgram import settings
from foodgram.tests.base_classes import UsersViewsSetupBase, ViewsTestBase

User = get_user_model()


class UsersViewsTest(ViewsTestBase, UsersViewsSetupBase):
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
                '/personal/auth/reset/MQ/set-password/',
                'registration/password_reset_confirm.html',
            ),
            (
                reverse('password_reset_complete'),
                'registration/password_reset_complete.html',
            ),
        ]
        self.check_template_used(reverse_names_templates)

    def test_object_list_in_context(self):
        favorites_queryset = self.user.favorites.all()
        purchases_queryset = self.user.purchases.all()
        subscriptions_queryset = self.user.subscriptions.all()

        start_index = 0
        stop_index = settings.PAGINATE_BY

        pages = [
            (
                reverse('users:favorite_list'),
                favorites_queryset, [start_index, stop_index],
            ),
            (
                reverse('users:purchase_list'),
                purchases_queryset, [None, None],
            ),
            (
                reverse('users:subscription_list'),
                subscriptions_queryset, [None, None],
            ),
        ]
        self.check_object_list_in_context(pages)
