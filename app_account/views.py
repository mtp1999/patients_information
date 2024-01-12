from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
# from .forms import CostumeUserCreationForm
from app_account.models import User


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = "app_account/login.html"

    def post(self, request, *args, **kwargs):
        user = authenticate(
            request, email=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            login(request, user)
            messages.success(request, "خوش آمدید!")
            if self.request.GET.get("next"):
                return redirect(self.request.GET.get("next"))
            return redirect("app_patient:home")
        else:
            messages.error(request, "اطلاعات وارد شده صحیح نمیباشد!")
            return redirect("app_account:login")


class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
            messages.success(request, "خروج با موفقیت انجام شد!")
            return redirect("app_account:login")
        except:
            messages.error(request, "خطا!")
            return redirect("app_patient:home")


# class SignUpView(LoginView):
#     redirect_authenticated_user = True
#     template_name = "app_account/signup.html"
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data["form"] = CostumeUserCreationForm
#         return data
#
#     def post(self, request, *args, **kwargs):
#         form = CostumeUserCreationForm(request.POST)
#         if form.is_valid():
#             user = User.objects.filter(email=form.cleaned_data["email"])
#             if user:
#                 messages.error(request, "Account exists,Try Again")
#                 return redirect("app_account:signup")
#             form.save()
#             messages.success(request, "Sign Up Successfully")
#             return redirect("app_account:login")
#         else:
#             messages.error(request, "Wrong Information,Try Again")
#             return redirect("app_account:signup")
