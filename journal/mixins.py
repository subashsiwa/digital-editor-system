from django.core.exceptions import PermissionDenied

class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_owner():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class EditorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_editor():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_author():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)