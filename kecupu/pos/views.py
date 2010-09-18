# Create your views here.
from django.contrib.auth.decorators import login_required
from kecupu.pos.utils import render_response, login_required

@login_required
def index(request):
    stores = tuple()
    return render_response(
        request,
        'kecupu.pos/index.html',
        {'stores': stores}
    )

@login_required
def new_order(request):
    items = (
        {'id': 1, 'name': 'NW1', 'qty': 2, 'price': 100.0},
    )
    items = tuple()
    return render_response(
        request,
        'kecupu.pos/new_order.html',
        {'items': items}
    )
