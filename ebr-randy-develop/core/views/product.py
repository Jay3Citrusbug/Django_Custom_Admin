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
from core.forms.product import ProductCreationForm,ProductChangeForm
from core.models import Product
from django.http import JsonResponse
from django.shortcuts import render
# -----------------------------------------------------------------------------
# BikeClass Views
# -----------------------------------------------------------------------------


class ProductListView(MyListView):
    """
    View for BikeClass listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = Product
    queryset = model.objects.all()
    template_name = "core/product/product_list.html"
    permission_required = ("core.view_product",)



class ProductCreateView(MyCreateView):
    """
    View to create product
    """
    model = Product
    form_class = ProductCreationForm
    template_name = "core/product/product_form.html"
    permission_required = ("core.add_product",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:product-list")


class ProductUpdateView(MyUpdateView):
    """
    View to update product
    """

    model = Product
    form_class = ProductChangeForm
    template_name = "core/product/product_form.html"
    permission_required = ("core.change_product",)

    def get_success_url(self):
        return reverse("core:product-list")


class ProductDeleteView(MyDeleteView):
    """
    View to delete product
    """
    model = Product
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_product",)

    def get_success_url(self):
        return reverse("core:product-list")


class ProductAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for FrameType
    """
    model = Product
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
                # Q(category__icontains=self.search) |
                Q(product_code__icontains=self.search)|
                Q(name__icontains=self.search)
            
                
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
                    "name":o.name,
                    "product_code":o.product_code,
                    "description":o.description,
                    "short_description":o.short_description,
                    "price":o.price,
                    "actions": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        total_filter_data = len(self.filter_queryset(self.model.objects.all().order_by("-id")))
        context_data['recordsTotal'] = len(self.model.objects.all().order_by("-id"))
        context_data['recordsFiltered'] = total_filter_data
        print(type(context_data),"------------------------------------------------")
        # try:
        return JsonResponse(context_data)
        # except Exception as e:
        #     print(e)
        #     return JsonResponse(str(e),safe=False)