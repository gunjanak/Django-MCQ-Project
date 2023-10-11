from functools import wraps
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def custom_permission_required(permission):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                if not request.user.has_perm(permission):
                    raise PermissionDenied
            except PermissionDenied:
                messages.error(request, "You do not have permission to access this page.")
                return redirect('MCQ_app:subject_list')  # Replace with the actual home URL

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
