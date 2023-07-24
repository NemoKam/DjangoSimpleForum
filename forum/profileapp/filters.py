from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import FieldError

class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        return ((),)
    
    def choices(self, changelist):
        all_choice = next(super().choices(changelist)) # type: ignore
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice

class IDFilter(InputFilter):
    parameter_name = 'id'
    title = _('ID')

    def queryset(self, request, queryset):
        if self.value() is not None:
            user_id = self.value()

            return queryset.filter(
                Q(id=user_id)
            )
        
class UsernameFilter(InputFilter):
    parameter_name = 'username'
    title = _('USERNAME')

    def queryset(self, request, queryset):
        if self.value() is not None:
            username = self.value()

            try:
                return queryset.filter(Q(username__contains=username))
            except FieldError:
                pass
            try:
                return queryset.filter(Q(author__username__contains=username))
            except FieldError:
                pass

    