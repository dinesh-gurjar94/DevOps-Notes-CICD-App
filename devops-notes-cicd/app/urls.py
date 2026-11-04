from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:pk>/edit/', views.edit_note, name='edit_note'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
    path('health/', views.health, name='health'),
]
