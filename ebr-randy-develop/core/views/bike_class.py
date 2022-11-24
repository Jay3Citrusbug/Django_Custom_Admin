# -*- coding: utf-8 -*-
"""
This is a view module to define list, create, update, delete views.

You can define different view properties here.
"""

from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from django.shortcuts import reverse

from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyListView, MyCreateView, MyUpdateView, MyDeleteView, MyLoginRequiredView,
)
from core.forms.bike_class import BikeClassCreationForm,BikeClassChangeForm
from core.models import BikeClass
from django.http import JsonResponse
from django.shortcuts import render
# -----------------------------------------------------------------------------
# BikeClass Views
# -----------------------------------------------------------------------------


class BikeClassListView(MyListView):
    """
    View for BikeClass listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = BikeClass
    queryset = model.objects.all()
    template_name = "core/Bike_Class/Bike_Class_list.html"
    permission_required = ("core.view_bikeclass",)



class BikeClassCreateView(MyCreateView):
    """
    View to create BikeClass
    """
    model = BikeClass
    form_class = BikeClassCreationForm
    template_name = "core/Bike_Class/Bike_Class_form.html"
    permission_required = ("core.add_bikeclass",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:bikeclass-list")


class BikeClassUpdateView(MyUpdateView):
    """
    View to update BikeClass
    """

    model = BikeClass
    form_class = BikeClassChangeForm
    template_name = "core/Bike_Class/Bike_Class_form.html"
    permission_required = ("core.change_bikeclass",)

    def get_success_url(self):
        return reverse("core:bikeclass-list")


class BikeClassDeleteView(MyDeleteView):
    """
    View to delete BikeClass
    """
    model = BikeClass
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_bikeclass",)

    def get_success_url(self):
        return reverse("core:bikeclass-list")


class BikeClassAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for BikeClass
    """
    model = BikeClass
    queryset = model.objects.all().order_by("-id")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("core/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def is_orderable(self):
        """Check if order is defined in dictionary."""
        # if self._querydict.get("order"):
        #     return True
        return True

    def _get_actions(self, obj):
        """Get actions column markup."""
        t = get_template("core/partials/list_row_actions.html")
        opts = self.model._meta
        return t.render({
            "o": obj,
            "opts": opts,
            "has_change_permission": self.has_change_permission(self.request),
            "has_delete_permission": self.has_delete_permission(self.request),
        })

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(name__icontains=self.search) |
                Q(slug__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "bike_class": o.bike_class,
                    "actions": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        total_filter_data = len(self.filter_queryset(self.model.objects.all().order_by("-id")))
        context_data['recordsTotal'] = len(self.model.objects.all().order_by("-id"))
        context_data['recordsFiltered'] = total_filter_data
        return JsonResponse(context_data)
