from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_owner():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def editor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_editor():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def author_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_author():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper