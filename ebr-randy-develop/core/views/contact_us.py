# -*- coding: utf-8 -*-
"""
This is a view module to define list, create, update, delete views.

You can define different view properties here.
"""
import datetime

from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from django.shortcuts import reverse, redirect

from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyListView, MyDetailView, MyCreateView, MyUpdateView, MyDeleteView, MyLoginRequiredView
)
# from core.forms import ContactUsCreationForm, ContactUsChangeForm
from core.models import ContactUs

from django.http import JsonResponse


# -----------------------------------------------------------------------------
# Page Views
# -----------------------------------------------------------------------------

class ContactUsListView(MyListView):
    """
    View for ContactUs listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = ContactUs
    queryset = model.objects.all()
    template_name = "core/contact_us/contactus_list.html"
    permission_required = ("core.view_contactus",)


class ContactUsCreateView(MyCreateView):
    """
    View to create ContactUs
    """
    model = ContactUs
    # form_class = ContactUsCreationForm
    template_name = "core/contactus/contactus_form.html"
    permission_required = ("core.add_contactus",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:contactus-list")


class ContactUsUpdateView(MyUpdateView):
    """
    View to update ContactUs
    """

    model = ContactUs
    # form_class = ContactUsChangeForm
    template_name = "core/contactus/contactus_form.html"
    permission_required = ("core.change_contactus",)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:contactus-list")


class ContactUsDeleteView(MyDeleteView):
    """
    View to delete ContactUs
    """
    model = ContactUs
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_contactus",)

    def get_success_url(self):
        return reverse("core:contactus-list")


class ContactUsAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for ContactUs
    """
    model = ContactUs
    queryset = model.objects.all().order_by("-id")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("core/partials/list_boolean.html")
        print("_get_is_superuser", obj.is_superuser)
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
        comment_data = self.request.GET.get('comment_data')
        print(comment_data)
        if comment_data == 'all':
            if self.search:
                return qs.filter(~Q(is_spam=True),
                    Q(name__icontains=self.search) | Q(email__icontains=self.search) | Q(message__icontains=self.search)
                )
            else:
                return qs.filter(~Q(is_spam=True))
        elif comment_data == 'spam':
            if self.search:
                return qs.filter(
                    Q(name__icontains=self.search) | Q(email__icontains=self.search) |
                    Q(message__icontains=self.search), is_spam=True
                )
            else:
                print('ele condition work...')
                return qs.filter(is_spam=True)
        else:
            if self.search:
                return qs.filter(
                    Q(name__icontains=self.search) | Q(email__icontains=self.search) |
                    Q(message__icontains=self.search)
                )
            else:
                return qs

    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "name": o.name,
                    "email": o.email,
                    "message": o.message,
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
