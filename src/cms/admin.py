from django.contrib import admin
from .models import Article, News, Document


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "short_description", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "short_description", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "doc_type", "document_date", "is_published")
    list_filter = ("doc_type", "is_published")
    search_fields = ("title", "short_description", "content")
    prepopulated_fields = {"slug": ("title",)}