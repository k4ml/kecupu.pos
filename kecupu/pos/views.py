# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect

from kecupu.pos.utils import render_response, login_required
from kecupu.pos.models import Customer, Order, OrderItem

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
    store_id = request.session['store_id']
    if request.method == 'POST':
        customer_id = request.POST['customer-id'].split("-")[0]
        item_id = request.POST['item-id'].split("-")[0]
        qty = request.POST['item-qty']
        order_id = request.POST['order-id']

        customer = Customer.objects.get(pk=customer_id)

        if order_id:
            order = Order.objects.get(pk=order_id)
        else:
            order = Order(customer=customer, total=1, store_id = store_id)
        order.save()
        order_item = OrderItem.objects.create(item_id=item_id, order=order, qty=qty)
        order_item.save()

    items = tuple()
    return render_response(
        request,
        'kecupu.pos/new_order.html',
        {'items': items}
    )

def current_order(request, id=None):
    items = tuple()
    if id is not None:
        order = Order.objects.get(pk=id)
        items = OrderItem.objects.filter(order__id=id)
    return render_response(
        request,
        'kecupu.pos/new_order.html',
        {'items': items, 'order': order,}
    )
    

@login_required
def customer_autocomplete(request):
    if 'term' in request.GET:
        keyword = request.GET['term']
        import simplejson

        customers = Customer.objects.filter(name__icontains=keyword)
        output = []
        for customer in customers:
            output.append({"id": customer.id, "value": customer.id, "label": customer.name})
        return HttpResponse(simplejson.dumps(output), mimetype='application/json')

@login_required
def item_autocomplete(request):
    if 'term' in request.GET:
        keyword = request.GET['term']
        from kecupu.pos.models import Item
        import simplejson

        items = Item.objects.filter(name__icontains=keyword)
        output = []
        for item in items:
            output.append({"id": item.id, "value": item.id, "label": item.name})
        return HttpResponse(simplejson.dumps(output), mimetype='application/json')
