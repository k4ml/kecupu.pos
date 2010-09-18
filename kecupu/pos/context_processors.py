
def site_global(request):
    context = {}
    if 'store_id' in request.session:
        store = request.user.store_set.all()[0]
        context['store'] = store
    return context
