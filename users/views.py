from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView
from users.models import User
import config.settings as settings

from users.forms import UserRegisterForm

from users.forms import UserProfileForm
from users.services import remove_jobs_by_user, add_jobs_by_user

UID_CONST = 27934


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_verified = False

        uid = new_user.pk
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uid': uid})
        activation_url = 'http://127.0.0.1:8000' + activation_url
        send_mail(
            subject='Подтверждение e-mail адреса',
            message=f'Для подтверждения аккаунта, пожалуйста, перейдите по ссылке: {activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class EmailConfirmEmailView(View):

    def get(self, request, uid):
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user.is_verified = True
            user.save()
            return redirect('users:profile')
        else:
            return redirect('/')


class PasswordResetView(TemplateView):
    template_name = 'users/password_reset.html'

    def post(self, request):
        email = self.request.POST.get('email')
        print(email)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if User is not None:
            password = User.objects.make_random_password(12)
            user.set_password(
                password
            )
            user.save()
            send_mail(
                subject='Сброс пароля',
                message=f'Ваш новый пароль:\n{password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            return redirect('users:login')
        else:
            return redirect('/')


class UserListView(PermissionRequiredMixin, ListView):
    model = User

    def has_permission(self):
        user = self.request.user
        return user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_staff=False)


class UserBlockView(PermissionRequiredMixin, View):

    def has_permission(self):
        user = self.request.user
        return user.is_staff

    def get(self, request, uid):
        print('DEBUG', uid)
        user = User.objects.get(pk=uid)
        print(user)
        user.is_active = not user.is_active
        user.save()
        if user.is_active:
            add_jobs_by_user(uid)
        else:
            remove_jobs_by_user(uid)
        return redirect('users:user_list')
