from django.shortcuts import render
from cms.models import Article, News
from materials.models import Material, MaterialType, Subject


def home(request):
    # Категории материалов (КТП, поурочные и т.д.)
    material_types = (
        MaterialType.objects
        .filter(is_active=True)
        .order_by("order", "title")
    )

    # Предметы
    subjects = (
        Subject.objects
        .filter(is_active=True)
        .order_by("order", "title")
    )

    # Классы 1–11 (пока фиксированные)
    grades = list(range(1, 12))

    # Последние материалы
    latest_materials = (
        Material.objects
        .filter(is_published=True)
        .select_related("subject", "material_type", "author")
        .order_by("-created_at")[:10]
    )

    # Последние статьи (для главной)
    latest_articles = (
        Article.objects
        .filter(is_published=True)
        .order_by("-created_at")[:5]
    )

    # Последние новости (опционально, если будем выводить)
    latest_news = (
        News.objects
        .filter(is_published=True)
        .order_by("-created_at")[:5]
    )

    return render(
        request,
        "core/home.html",
        {
            "material_types": material_types,
            "subjects": subjects,
            "grades": grades,
            "latest_materials": latest_materials,
            "latest_articles": latest_articles,
            "latest_news": latest_news,
        }
    )