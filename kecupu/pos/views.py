# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages

from kecupu.pos.utils import render_response, login_required
from kecupu.pos.models import Customer, Order, OrderItem, Item, \
    Payment
    

def _go_to_current_order(request, order):
    return HttpResponseRedirect(reverse('kecupu.pos.views.current_order', args=[order.id]))

def orders(request):
    customer_id = None
    orders = ()
    error = None
    if 'customer-id' in request.GET:
        customer_id = request.GET.get('customer-id').split("-")[0]
    if customer_id:
        orders = Order.objects.filter(customer__id__exact=customer_id)
        if not orders:
            error = 'No orders found'
    return render_response(
        request,
        'kecupu.pos/orders.html',
        {'orders': orders, 'error': error}
    )

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
        item = get_object_or_404(Item, pk=item_id)

        if not qty:
            messages.add_message(request, messages.ERROR, 'Qty field is required')
            return _go_to_current_order(request, order)

        order_item = OrderItem.objects.create(item_id=item_id, order=order, qty=qty, price=item.price)
        order_item.save()
        return _go_to_current_order(request, order)
    return HttpResponseNotAllowed(['POST'])

@login_required
def current_order(request, id=None):
    from django.db.models import Sum, F
    orderitems = tuple()

    if id is not None:
        order = get_object_or_404(Order, pk=id)
        orderitems = order.orderitem_set.all()
        order.save()

        try:
            payment = order.payment_set.all()[0]
        except:
            payment = {};

    return render_response(
        request,
        'kecupu.pos/new_order.html',
        {
            'orderitems': orderitems, 
            'order': order,
            'payment': payment,
        }
    )
    
@login_required
def update_order(request, id=None):
    order = get_object_or_404(Order, pk=id)

    if request.method == 'POST':
        for orderitem in order.orderitem_set.all():
            remove = request.POST.get('item-remove-%s' % orderitem.id)
            if remove:
                orderitem.delete()
            qty = request.POST.get('item-qty-%s' % orderitem.id)
            if qty:
                orderitem.qty = int(qty)
                orderitem.save()
        order.save()

        payment_amount = None
        payment_method = 'Cash'
        payment_checque = None

        if 'payment-amount' in request.POST:
            payment_amount = request.POST.get('payment-amount')
        if 'payment-checque' in request.POST:
            payment_checque = request.POST.get('payment-checque')
        if 'payment-method' in request.POST:
            payment_method = request.POST.get('payment-method')


        if payment_amount:
            try:
                float(payment_amount)
            except ValueError:
                messages.add_message(request, messages.ERROR, 'Invalid amount')
                return _go_to_current_order(request, order)
                
            if payment_method == 'Cash' and payment_checque:
                messages.add_message(request, messages.ERROR, 'Please select Cheque as payment method')
                return _go_to_current_order(request, order)
            if payment_method == 'Checque' and not payment_checque:
                messages.add_message(request, messages.ERROR, 'Please enter Checque No')
                return _go_to_current_order(request, order)
            payment = Payment.objects.create(order_id=order.id, method=payment_method, checque_no=payment_checque, amount=payment_amount)
            if payment.save():
                messages.add_message(request, messages.SUCCESS, 'Payment added')

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
