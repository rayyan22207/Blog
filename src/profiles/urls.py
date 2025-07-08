from . import views
from django.urls import path

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile_view'),
    path('edit/', views.edit_profile, name='edit_profile'),
]
