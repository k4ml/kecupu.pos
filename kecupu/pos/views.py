# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render_to_response(
        'kecupu.pos/index.html',
        {},
        context_instance=RequestContext(request)
    )

@login_required
def new_order(request):
    items = (
        {'id': 1, 'name': 'NW1', 'qty': 2, 'price': 100.0},
    )
    items = tuple()
    return render_to_response(
        'kecupu.pos/new_order.html',
        {'items': items},
        context_instance=RequestContext(request)
    )
