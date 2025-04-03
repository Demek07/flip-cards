from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from flip_cards_app.views import MenuMixin
from flip_cards_app.models import Word
from .forms import RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, CustomAuthenticationForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EmailActivationToken
from .utils import send_activation_email


from django.views import View


class ActivateAccountView(MenuMixin, TemplateView):
    """
    Представление для активации аккаунта пользователя по токену
    """
    template_name = 'users/activation_success.html'  # По умолчанию

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if not token:
            messages.error(request, 'Недействительная ссылка активации.')
            self.template_name = 'users/activation_error.html'
            kwargs['error_message'] = 'Недействительная ссылка активации.'
            return super().get(request, *args, **kwargs)

        try:
            activation = EmailActivationToken.objects.get(token=token)
            if not activation.is_valid():
                messages.error(request, 'Срок действия ссылки активации истек. Пожалуйста, запросите новую ссылку.')
                self.template_name = 'users/activation_error.html'
                kwargs['error_message'] = 'Срок действия ссылки активации истек. Пожалуйста, запросите новую ссылку.'
                return super().get(request, *args, **kwargs)

            user = activation.user
            user.is_active = True
            user.save()

            # Удаляем использованный токен
            activation.delete()

            # Устанавливаем шаблон успешной активации
            self.template_name = 'users/activation_success.html'
            kwargs['user'] = user
            return super().get(request, *args, **kwargs)

        except EmailActivationToken.DoesNotExist:
            messages.error(request, 'Недействительная ссылка активации.')
            self.template_name = 'users/activation_error.html'
            kwargs['error_message'] = 'Недействительная ссылка активации.'
            return super().get(request, *args, **kwargs)


class LoginUser(MenuMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('catalog')


class RegisterUser(MenuMixin, CreateView):
    """
    Представление для регистрации пользователя с отправкой email для активации
    """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_done')  # Изменено на страницу входа

    def form_valid(self, form):
        # Сохраняем пользователя (он будет неактивным благодаря переопределенному методу save в форме)
        response = super().form_valid(form)
        user = self.object

        # Создаем токен активации
        token = EmailActivationToken.objects.create(user=user)

        # Отправляем email с ссылкой активации
        send_activation_email(self.request, user, token.token)

        # Добавляем сообщение об успешной регистрации
        messages.success(self.request, 'Регистрация успешна! На ваш email отправлена ссылка для активации аккаунта.')

        return response


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
