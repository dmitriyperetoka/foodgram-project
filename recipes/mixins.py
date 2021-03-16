from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class IsAuthorPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def has_permission(self):
        return self.get_object().author_id == self.request.user.id  # noqa
