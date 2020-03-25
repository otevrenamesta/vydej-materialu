from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from .forms import DispensedForm, DispenseItemForm, DispenseStartForm, LoginForm
from .models import Dispensed, Location, LocationStaff, Material, Region


class AboutView(TemplateView):
    template_name = "main/about.html"


class RegistrationView(TemplateView):
    template_name = "main/under_construction.html"


class PasswordResetView(TemplateView):
    template_name = "main/under_construction.html"


class LoginView(FormView):
    template_name = "main/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data["email"], password=form.cleaned_data["password"],
        )
        if user is not None:
            login(self.request, user)
            self.request.session["location_id"] = form.cleaned_data["location"].id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:dispense")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("main:login"))


class DispenseView(LoginRequiredMixin, FormView):
    template_name = "main/dispense_overview.html"
    history_limit = 10
    form_class = DispenseStartForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dispensed"] = Dispensed.objects.filter(
            location_id=self.request.session["location_id"]
        )[: self.history_limit]
        return context

    def get(self, request, *args, **kwargs):
        if "location_id" not in self.request.session:
            return redirect(reverse("main:logout"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.id_card_no = form.cleaned_data["id_card_no"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:dispense_new", kwargs={"id_card_no": self.id_card_no})


class DispenseNewView(LoginRequiredMixin, TemplateView):
    template_name = "main/dispense_new.html"

    def get_materials(self):
        return Material.get_available(self.request.session["location_id"])

    def get_context_data(self, id_card_no, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id_card_no"] = id_card_no
        context["forms"] = [DispenseItemForm(mat) for mat in self.get_materials()]
        return context

    def post(self, request, id_card_no, *args, **kwargs):
        for material in self.get_materials():
            form = DispenseItemForm(material, request.POST)
            if form.is_valid() and form.cleaned_data["quantity"] > 0:
                Dispensed.objects.create(
                    material=material,
                    user=request.user,
                    location_id=request.session["location_id"],
                    quantity=form.cleaned_data["quantity"],
                    id_card_no=id_card_no,
                )
        return redirect(reverse("main:dispense"))


class DispenseEditView(LoginRequiredMixin, UpdateView):
    template_name = "main/dispense_edit.html"
    model = Dispensed
    fields = ["id_card_no", "quantity"]

    def get_success_url(self):
        return reverse("main:dispense")


class RegionListView(ListView):
    template_name = "main/region-list.html"
    model = Region

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=Region.ACTIVE)


class RegionView(DetailView):
    template_name = "main/region.html"
    model = Region
    slug_field = "id"
    slug_url_kwarg = "id"


class LocationView(DetailView):
    template_name = "main/location.html"
    model = Location
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["volunteers"] = self.object.staff.filter(
            locationstaff__status=LocationStaff.VOLUNTEER
        )
        ctx["admins"] = self.object.staff.filter(
            locationstaff__status=LocationStaff.ADMIN
        )
        ctx["pending"] = self.object.staff.filter(
            locationstaff__status=LocationStaff.PENDING
        )
        return ctx
