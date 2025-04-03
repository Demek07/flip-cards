from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    photo = models.ImageField(upload_to='users/images/%Y/%m/%d/', blank=True, null=True, verbose_name='Фотография')
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения')

    def __str__(self):
        return self.username


class EmailActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Проверка срока действия токена
        expiration_days = getattr(settings, 'EMAIL_ACTIVATION_TIMEOUT_DAYS', 7)
        return (timezone.now() - self.created_at).days <= expiration_days
