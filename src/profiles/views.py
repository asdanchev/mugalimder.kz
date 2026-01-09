from django.http import HttpResponse

def teacher_profile_view(request, token):
    return HttpResponse(f"Профиль с токеном: {token}")