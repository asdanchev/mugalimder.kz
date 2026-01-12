from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseContent(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_description = models.TextField(blank=True)
    content = models.TextField()

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Article(BaseContent):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta(BaseContent.Meta):
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class News(BaseContent):
    source_url = models.URLField(blank=True)

    class Meta(BaseContent.Meta):
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Document(BaseContent):
    doc_type = models.CharField(max_length=100, help_text="Например: Приказ, Постановление, Правила")
    document_date = models.DateField(null=True, blank=True)
    official_url = models.URLField()

    class Meta(BaseContent.Meta):
        verbose_name = "Документы"
        verbose_name_plural = "Документы"