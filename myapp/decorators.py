# decorators.py
from django.http import HttpResponseRedirect
from django.urls import reverse

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):  # Check if the user is logged in using session
            return HttpResponseRedirect(reverse('login'))  # Redirect to login page if not authenticated
        return view_func(request, *args, **kwargs)  # Proceed to the view if logged in
    return wrapper
