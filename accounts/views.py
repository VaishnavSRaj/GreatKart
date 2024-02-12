from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from urllib.parse import quote
from .forms import RegistrationForm
from .models import Account

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            user = Account.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone_number=form.cleaned_data["phone_number"],
                email=email,
                password=password,
            )
            user.save()

            # user activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string(
                "account/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_mail = email
            sent_mail = EmailMessage(mail_subject, message, to=[to_mail])
            sent_mail.send()
            # return redirect("/account/login/?command=verification=" + email)
            return redirect(
                reverse("login") + "?command=verification&email=" + quote(email)
            )

    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "account/register.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    return render(request, "account/login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("logout")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


def dashboard(request):
    return render(request, "account/dashboard.html")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset Password"
            message = render_to_string(
                "account/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_mail = email
            sent_mail = EmailMessage(mail_subject, message, to=[to_mail])
            sent_mail.send()
            messages.success(
                request, "reset password link has sent to you email address"
            )
            return redirect("login")
        else:
            messages.error(request, "Email address not found")
            return redirect("forgot_password")
    return render(request, "account/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["udi"] = uid
        messages.success(request, "Please reset your password")
        return redirect("resetPassword")
    else:
        messages.error(request, "This link has been expired")
        return redirect("login")


def resetPassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = request.session.get("udi")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully")
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("resetPassword")
    else:
        return render(request, "account/resetPassword.html")
