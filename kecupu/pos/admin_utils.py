from django.contrib import admin
from django.http import HttpResponseRedirect

class ButtonableModelAdmin(admin.ModelAdmin):
    """
    A subclass of this admin will let you add buttons (like history)    in the change view of an entry.
    http://djangosnippets.org/snippets/1016/

    ex.
    class FooAdmin(ButtonableModelAdmin):
      ...

      def bar(self, obj):
         obj.bar()
      bar.short_description='Example button'

      buttons = [ bar ]

    """
    buttons=()

    def change_view(self, request, object_id, extra_context={}): 
        extra_context['buttons']=self.buttons 
        return super(ButtonableModelAdmin, self).change_view(request, object_id, extra_context)

    def button_view_dispatcher(self, request, object_id, command): 
        obj = self.model._default_manager.get(pk=object_id) 
        return getattr(self, command)(request, obj)  \
            or HttpResponseRedirect(request.META['HTTP_REFERER'])

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        from django.utils.functional import update_wrapper

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        return patterns('',
            *(url(r'^(\d+)/(%s)/$' % but.func_name, wrap(self.button_view_dispatcher)) for but in self.buttons)
        ) + super(ButtonableModelAdmin, self).get_urls()
