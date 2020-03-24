from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, View

from .forms import DispensedForm, DispenseNewForm, DispenseStartForm, LoginForm
from .models import Dispensed, Location, LocationStaff, Material, Region


class AboutView(TemplateView):
    template_name = "main/about.html"


class RegistrationView(TemplateView):
    template_name = "main/under_construction.html"


class PasswordResetView(TemplateView):
    template_name = "main/under_construction.html"


class LoginView(TemplateView):
    template_name = "main/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                request.session["location_id"] = form.cleaned_data["location"].id
                return redirect(reverse("main:dispense"))
        return redirect(reverse("main:login"))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("main:login"))


class DispenseView(LoginRequiredMixin, TemplateView):
    template_name = "main/dispense_overview.html"
    history_limit = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["dispensed"] = Dispensed.objects.filter(
            location_id=self.request.session["location_id"]
        )[: self.history_limit]

        context["form"] = DispenseStartForm()

        return context

    def get(self, request, *args, **kwargs):
        if "location_id" not in self.request.session:
            return redirect(reverse("main:logout"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = DispenseStartForm(request.POST)
        if form.is_valid():
            id_card_no = form.cleaned_data["id_card_no"]
            return redirect(
                reverse("main:dispense_new", kwargs={"id_card_no": id_card_no})
            )
        return redirect(reverse("main:dispense"))


class DispenseNewView(LoginRequiredMixin, TemplateView):
    template_name = "main/dispense_new.html"

    def get_context_data(self, id_card_no, **kwargs):
        context = super().get_context_data(**kwargs)

        context["id_card_no"] = id_card_no

        context["form"] = DispenseNewForm()
        context["form"].fields["material"].queryset = Material.objects.filter(
            region__location__id=self.request.session["location_id"]
        )

        return context

    def post(self, request, id_card_no, *args, **kwargs):
        form = DispenseNewForm(request.POST)
        if form.is_valid():
            Dispensed.objects.create(
                material=form.cleaned_data["material"],
                user=request.user,
                location_id=request.session["location_id"],
                quantity=form.cleaned_data["quantity"],
                id_card_no=id_card_no,
            )
            return redirect(reverse("main:dispense"))
        return redirect(reverse("main:dispense_new", kwargs={"id_card_no": id_card_no}))


class DispenseEditView(LoginRequiredMixin, UpdateView):
    model = Dispensed
    form_class = DispensedForm
    template_name = "main/dispense_edit.html"


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
