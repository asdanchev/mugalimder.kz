from django.db import models
from django.contrib.auth.models import User
import uuid

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    full_name = models.CharField("Полное имя", max_length=255)
    bio = models.TextField("О себе", blank=True)
    is_premium = models.BooleanField("Премиум-доступ", default=False)
    token = models.CharField("Токен профиля", max_length=64, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex[:10]  # короткий токен
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.user.username

    class Meta:
        verbose_name = "Профиль учителя"
        verbose_name_plural = "Профили учителей"