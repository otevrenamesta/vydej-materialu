from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, View

from .forms import DispensedForm, DispenseNewForm, DispenseStartForm, LoginForm
from .models import Dispensed, Material


class HomeView(TemplateView):
    template_name = "main/home.html"


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
                username=form.cleaned_data["username"],
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
