# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse

from kecupu.pos.utils import render_response, login_required
from kecupu.pos.models import Customer, Order, OrderItem

def _go_to_current_order(request, order):
    return HttpResponseRedirect(reverse('kecupu.pos.views.current_order', args=[order.id]))

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
    if request.method == 'POST':
        store_id = request.session['store_id']
        customer_id = request.POST['customer-id'].split("-")[0]
        customer = get_object_or_404(Customer, pk=customer_id)
        order = Order(customer=customer, total=1, store_id = store_id)
        order.save()
        return _go_to_current_order(request, order)
    items = tuple()
    return render_response(
        request,
        'kecupu.pos/new_order.html',
        {'items': items}
    )

@login_required
def add_order_item(request, order_id):
    if request.method == 'POST':
        item_id = request.POST['item-id'].split("-")[0]
        qty = request.POST['item-qty']

        order = get_object_or_404(Order, pk=order_id)
        order_item = OrderItem.objects.create(item_id=item_id, order=order, qty=qty)
        order_item.save()
        return _go_to_current_order(request, order)
    return HttpResponseNotAllowed(['POST'])

@login_required
def current_order(request, id=None):
    items = tuple()
    if id is not None:
        order = get_object_or_404(Order, pk=id)
        items = OrderItem.objects.filter(order__id=id)
    return render_response(
        request,
        'kecupu.pos/new_order.html',
        {'items': items, 'order': order,}
    )
    
@login_required
def update_order(request, id=None):
    order = get_object_or_404(Order, pk=id)

    if request.method == 'POST':
        for item in order.items.all():
            remove = request.POST.get('item-remove-%s' % item.id)
            if remove:
                OrderItem.objects.filter(item__id__exact=item.id, order__id__exact=order.id).delete()
            qty = request.POST.get('item-qty-%s' % item.id)
            if qty:
                OrderItem.objects.filter(item__id__exact=item.id, order__id__exact=order.id).update(qty=qty)

        return HttpResponseRedirect(reverse('kecupu.pos.views.current_order', args=[order.id]))

    return HttpResponseNotAllowed(['POST'])


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
