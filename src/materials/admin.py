from django.contrib import admin
from .models import Subject, MaterialType, Material


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order", "is_active", "show_on_home")
    list_editable = ("order", "is_active", "show_on_home")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "grade",
        "subject",
        "material_type",
        "author",
        "is_published",
        "created_at",
    )
    list_filter = ("grade", "subject", "material_type", "is_published")
    search_fields = ("title", "description")