from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import iri_to_uri

from .forms import MaterialForm
from .models import Material, MaterialType, Subject


def materials_home(request):
    material_types = MaterialType.objects.filter(is_active=True, show_on_home=True).order_by("order", "title")
    subjects = Subject.objects.filter(is_active=True).order_by("order", "title")
    grades = list(range(1, 12))
    return render(
        request,
        "materials/home.html",
        {"material_types": material_types, "subjects": subjects, "grades": grades},
    )


def materials_list(request):
    type_slug = (request.GET.get("type") or "").strip()
    subject_slug = (request.GET.get("subject") or "").strip()
    grade_raw = (request.GET.get("grade") or "").strip()

    qs = Material.objects.filter(is_published=True).select_related("subject", "material_type", "author")

    selected_type = None
    selected_subject = None
    selected_grade = None

    if type_slug:
        selected_type = get_object_or_404(MaterialType, slug=type_slug, is_active=True)
        qs = qs.filter(material_type=selected_type)

    if subject_slug:
        selected_subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
        qs = qs.filter(subject=selected_subject)

    if grade_raw.isdigit():
        selected_grade = int(grade_raw)
        qs = qs.filter(grade=selected_grade)

    material_types = MaterialType.objects.filter(is_active=True).order_by("order", "title")
    subjects = Subject.objects.filter(is_active=True).order_by("order", "title")
    grades = list(range(1, 12))

    return render(
        request,
        "materials/list.html",
        {
            "materials": qs,
            "material_types": material_types,
            "subjects": subjects,
            "grades": grades,
            "selected_type": selected_type,
            "selected_subject": selected_subject,
            "selected_grade": selected_grade,
        },
    )


@login_required(login_url="/auth/login/")
def material_create(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect("materials-list")
    else:
        form = MaterialForm()

    return render(request, "materials/create.html", {"form": form})


@login_required(login_url="/auth/login/")
def material_download(request, pk: int):
    material = get_object_or_404(Material, pk=pk, is_published=True)

    # Внешняя ссылка — просто редиректим (но только после логина)
    if material.external_url:
        return redirect(iri_to_uri(material.external_url))

    # Локальный файл — отдаём как attachment
    if material.file:
        try:
            return FileResponse(material.file.open("rb"), as_attachment=True)
        except FileNotFoundError:
            raise Http404("Файл не найден")

    raise Http404("Источник материала не задан")