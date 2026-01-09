from django.contrib import admin
from django.urls import path, include
from profiles.views import teacher_profile_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('users.urls')),

    path('p/<str:token>/', teacher_profile_view, name='teacher-profile'),

    path('', include('core.urls')),

    path("materials/", include("materials.urls")),
]