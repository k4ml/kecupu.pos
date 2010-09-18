from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required as login_required_orig

def render_response(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)

def login_required(func):
    @login_required_orig
    def decorator(request, *args, **kwargs):
        stores = request.user.store_set.all()
        if len(stores) == 1:
            request.session['store_id'] = stores[0].id
        return func(request, *args, **kwargs)
    return decorator
