# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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

@login_required
def customer_autocomplete(request):
    if 'term' in request.GET:
        keyword = request.GET['term']
        from kecupu.pos.models import Customer
        import simplejson

        customers = Customer.objects.filter(name__icontains=keyword)
        output = []
        for customer in customers:
            output.append({"id": customer.id, "value": customer.id, "label": customer.name})
        return HttpResponse(simplejson.dumps(output), mimetype='application/json')
