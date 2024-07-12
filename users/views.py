from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from flip_cards_app.views import MenuMixin
from flip_cards_app.models import Word
from .forms import RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, CustomAuthenticationForm
from verify_email.email_handler import send_verification_email
from django.shortcuts import redirect, render


class SendEmail:
    def __init__(self, user: User):
        self.user = user
        self.current_site = Site.objects.get_current().domain
        self.token = default_token_generator.make_token(self.user)
        self.uid = urlsafe_base64_encode(str(self.user.pk).encode())

    def send_activate_email(self):
        reset_password_url = reverse_lazy(
            "users:signup_confirm", kwargs={"uidb64": self.uid, "token": self.token}
        )
        subject = f"Активация аккаунта на сайте {self.current_site}"
        message = (
            f"Благодарим за регистрацию на сайте {self.current_site}.\n"
            "Для активации учётной записи, пожалуйста перейдите по ссылке:\n"
            f"https://{self.current_site}{reset_password_url}\n"
        )

        self.user.email_user(subject=subject, message=message)


class SignupConfirmView(MenuMixin, TemplateView):
    template_name = 'users/signup_confirm.html'
    extra_context = {'title': 'Подтверждение регистрации'}

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, self.template_name, {'verified': True})
        else:
            return render(request, self.template_name, {'verified': False})


class VerifyEmailView(MenuMixin, TemplateView):
    template_name = 'users/verify_email.html'
    extra_context = {'title': 'Подтверждение электронной почты'}

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, self.template_name, {'verified': True})
        else:
            return render(request, self.template_name, {'verified': False})


class ResendVerificationEmail(MenuMixin, LoginRequiredMixin, TemplateView):
    template_name = 'users/resend_verification_email.html'
    extra_context = {'title': 'Повторная отправка письма подтверждения'}

    def get(self, request):
        if request.user.is_active:
            return redirect(reverse_lazy('catalog'))
        return super().get(request)

    def post(self, request):
        user = request.user
        SendEmail(user).send_activate_email()
        return render(request, self.template_name, {'sent': True})


class LoginUser(MenuMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if not request.user.is_active:
            return render(request, 'users/not_active.html', {'title': 'Аккаунт не активен'})
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('catalog')


class RegisterUser(MenuMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_done')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Деактивируем пользователя до подтверждения email
        user.save()
        SendEmail(user).send_activate_email()  # Отправляем email для активации
        return redirect(self.success_url)


class RegisterDoneView(MenuMixin, TemplateView):
    template_name = 'users/register_done.html'
    extra_context = {'title': 'Регистрация завершена'}


class ProfileUser(MenuMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()  # Используем модель текущего пользователя
    form_class = ProfileUserForm  # Связываем с формой профиля пользователя
    template_name = 'users/profile.html'  # Указываем путь к шаблону
    # Дополнительный контекст для передачи в шаблон
    extra_context = {'title': 'Профиль пользователя', 'active_tab': 'profile'}

    def get_success_url(self):
        # URL, на который переадресуется пользователь после успешного обновления
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # Возвращает объект модели, который должен быть отредактирован
        return self.request.user


class PasswordChange(MenuMixin, LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Изменение пароля',
                     'active_tab': 'password_change'}
    success_url = reverse_lazy('users:password_change_done')


class PasswordChangeDone(MenuMixin, LoginRequiredMixin, TemplateView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Пароль изменен успешно'}


class UserCardsView(MenuMixin, LoginRequiredMixin, ListView):
    model = Word
    template_name = 'users/profile_cards.html'
    context_object_name = 'words'
    extra_context = {'title': 'Мои слова',
                     'active_tab': 'profile_cards'}

    # def get_queryset(self):
    # return Card.objects.filter(author=self.request.user).order_by('-upload_date')
