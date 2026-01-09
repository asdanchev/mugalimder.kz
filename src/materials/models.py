from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Subject(models.Model):
    title = models.CharField("Предмет", max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.title


class MaterialType(models.Model):
    title = models.CharField("Тип материала", max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_on_home = models.BooleanField("Показывать на главной", default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Тип материала"
        verbose_name_plural = "Типы материалов"

    def __str__(self):
        return self.title


class Material(models.Model):
    GRADE_CHOICES = [(i, f"{i} класс") for i in range(1, 12)]

    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)

    grade = models.PositiveSmallIntegerField("Класс", choices=GRADE_CHOICES)

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="materials",
        verbose_name="Предмет",
    )

    material_type = models.ForeignKey(
        MaterialType,
        on_delete=models.PROTECT,
        related_name="materials",
        verbose_name="Тип материала",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="Автор",
    )

    file = models.FileField(
        "Файл",
        upload_to="materials/%Y/%m/",
        blank=True,
        null=True,
    )

    external_url = models.URLField(
        "Внешняя ссылка",
        blank=True,
    )

    is_published = models.BooleanField("Опубликован", default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def clean(self):
        super().clean()

        has_file = bool(self.file)
        has_url = bool(self.external_url)

        if not has_file and not has_url:
            raise ValidationError("Нужно указать либо файл, либо ссылку.")

        if has_file and has_url:
            raise ValidationError("Можно указать только файл ИЛИ ссылку.")

    def __str__(self):
        return self.title